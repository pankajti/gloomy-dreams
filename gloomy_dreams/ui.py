from nicegui import ui

def render_ui(state):
    ui.label(f"Sentiment Summary for {state['ticker']}")
    for title, summary, sentiment in zip(state['articles'], state['summaries'], state['sentiments']):
        with ui.card():
            ui.label(f"📰 {title}")
            ui.label(f"📄 Summary: {summary}")
            ui.label(f"📊 Sentiment: {sentiment}")
