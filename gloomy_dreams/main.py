from nicegui import ui
from gloomy_dreams.graph import create_finance_graph
from gloomy_dreams.ui import render_ui

graph = create_finance_graph()

def run_pipeline(ticker):
    state = {"ticker": ticker}
    result = graph.invoke(state)
    render_ui(result)

with ui.card():
    ui.label("Agentic AI: Financial News Sentiment Analyzer")
    ticker_input = ui.input("Enter stock ticker", placeholder="e.g., AAPL")
    ui.button("Analyze", on_click=lambda: run_pipeline(ticker_input.value))

ui.run()
