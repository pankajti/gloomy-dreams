import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import datetime
import asyncio
import os

from gloomy_dreams.graph import create_finance_graph

# --- Setup Graph ---
graph = create_finance_graph()


# --- Export Graphviz diagram only if missing ---
def export_graph_image(graph_obj, output_path: str = "assets/graph_structure.png"):
    if os.path.exists(output_path):
        print(f"[INFO] Graph image already exists at {output_path}. Skipping regeneration.")
        return
    try:
        if hasattr(graph_obj, 'get_graph'):
            g = graph_obj.get_graph()
            if hasattr(g, 'draw_png'):
                g.draw_png(output_path)
                print(f"[INFO] Graph structure image saved to {output_path}")
            else:
                print("[ERROR] Graph missing 'draw_png' method.")
        else:
            print("[ERROR] Graph missing 'get_graph' method.")
    except Exception as e:
        print(f"[ERROR] Failed to generate graph image: {e}")


os.makedirs("assets", exist_ok=True)
export_graph_image(graph)

# --- Initialize App ---
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
server = app.server

# --- Layout ---
app.layout = html.Div([
    html.Div([
        html.H2("Gloomy Dreams", style={'margin-bottom': '30px'}),
        html.Button("Sentiment Analysis", id="sentiment-btn", n_clicks=0,
                    style={'width': '100%', 'margin-bottom': '10px'}),
        html.Button("Project Details", id="details-btn", n_clicks=0, style={'width': '100%', 'margin-bottom': '10px'}),
    ], style={'width': '20%', 'background-color': '#f0f0f0', 'padding': '20px', 'height': '100vh', 'flex-shrink': '0'}),

    html.Div(id="page-content", style={'width': '80%', 'padding': '40px', 'overflow-y': 'scroll', 'height': '100vh'})
], style={'display': 'flex'})

# --- Pages ---

sentiment_page = html.Div([
    html.H1("Agentic AI: Financial News Sentiment Analyzer", style={'textAlign': 'center'}),
    dcc.Input(id='ticker-input', type='text', placeholder='Enter stock ticker',
              style={'width': '300px', 'margin': '20px'}),
    html.Button('Analyze', id='analyze-btn', n_clicks=0),

    dcc.Loading(
        id="loading-wrapper",
        type="circle",
        fullscreen=False,  # ✅ Not fullscreen anymore!
        color="#119DFF",
        children=[
            html.Div(id='loading-text', style={'margin-top': '20px', 'fontStyle': 'italic', 'fontSize': '18px'}),
            html.Div(id='analysis-result', style={'margin-top': '20px'})
        ]
    )
])

details_page = html.Div([
    html.H1("About This Project", style={'textAlign': 'center'}),
    html.P("""
    This application uses an agentic AI system built with LangGraph and Dash
    to perform financial news sentiment analysis.
    It retrieves real-world financial news, summarizes using local LLMs,
    classifies sentiment, and presents a clean, dynamic UI.
    """, style={'maxWidth': '600px', 'margin': 'auto'}),

    html.H2("Workflow Diagram", style={'textAlign': 'center', 'margin-top': '40px'}),
    html.Img(src="/assets/graph_structure.png", style={'width': '20%', 'margin': 'auto', 'display': 'block'}),
    # ✅ 50% width and centered

    html.Div([
        html.A("🌐 GitHub", href="https://github.com/pankajti/gloomy-dreams", target="_blank",
               style={'margin-right': '20px'}),
        html.A("🔗 LinkedIn", href="https://www.linkedin.com/in/pankajti/", target="_blank")
    ], style={'textAlign': 'center', 'margin-top': '20px'})
])


# --- Callbacks ---

@app.callback(
    Output('page-content', 'children'),
    Input('sentiment-btn', 'n_clicks'),
    Input('details-btn', 'n_clicks')
)
def switch_page(sentiment_clicks, details_clicks):
    if details_clicks > sentiment_clicks:
        return details_page
    return sentiment_page


@app.callback(
    Output('loading-text', 'children'),
    Output('analysis-result', 'children'),
    Input('analyze-btn', 'n_clicks'),
    State('ticker-input', 'value'),
    prevent_initial_call=True
)
def run_analysis(n_clicks, ticker):
    if not ticker:
        return "", "Please enter a valid stock ticker."

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Step 1: Show fetching message
        loading_message = "Fetching latest news articles..."
        loading_text_output = loading_message
        result_output = html.Div()

        state = {
            "ticker": ticker,
            "retrieved_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        loop.run_until_complete(asyncio.sleep(0.5))  # Allow UI to update

        # Step 2: Update loading message
        loading_message = "Summarizing and analyzing sentiment..."
        loading_text_output = loading_message

        result = loop.run_until_complete(asyncio.to_thread(graph.invoke, state))

        loop.run_until_complete(asyncio.sleep(0.5))

        # Step 3: Build cards
        cards = []
        articles = result.get('articles', [])
        summaries = result.get('summaries', [])
        sentiments = result.get('sentiments', [])

        for idx, (article, summary, sentiment) in enumerate(zip(articles, summaries, sentiments)):
            safe_article_title = str(article)[:80] if article else "No Title Available"

            sentiment_lower = sentiment.lower()
            color = 'success' if 'positive' in sentiment_lower else 'danger' if 'negative' in sentiment_lower else 'secondary'

            cards.append(
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.Strong(f"News {idx + 1}: ", style={'margin-right': '5px'}),
                            html.Span(safe_article_title),
                        ]),
                        dbc.Badge(sentiment, color=color, className="ms-auto", pill=True)
                    ], className="d-flex justify-content-between align-items-center"),

                    dbc.CardBody([
                        html.P(summary, className="card-text", style={'fontSize': '16px', 'color': '#333'})
                    ])
                ], style={'margin-bottom': '20px', 'box-shadow': '0px 4px 8px rgba(0,0,0,0.1)',
                          'border-radius': '10px'})
            )

        result_output = dbc.Container(cards)

    except Exception as e:
        result_output = f"Error: {e}"
    finally:
        loop.close()

    return "", result_output


# --- Run ---

