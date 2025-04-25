from nicegui import ui
from datetime import datetime

def sentiment_color(label: str) -> str:
    label = label.lower()
    if "positive" in label:
        return "green"
    elif "negative" in label:
        return "red"
    return "gray"

def render_ui(state: dict):
    ui.label(f"🧠 Sentiment Summary for: {state['ticker']}").classes('text-xl font-bold')

    if "retrieved_at" in state:
        ui.label(f"🕒 Data retrieved on: {state['retrieved_at']}")

    for title, summary, sentiment in zip(state["articles"], state["summaries"], state["sentiments"]):
        with ui.card():
            ui.label(f"📰 {title}").classes('text-md font-semibold')
            ui.label(f"📄 {summary}")
            ui.label("📊 Sentiment:").classes('font-bold')
            ui.label(sentiment).style(f"color: {sentiment_color(sentiment)}")
