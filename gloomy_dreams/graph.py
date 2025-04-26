from typing import TypedDict, List
from langgraph.graph import StateGraph,START,END

from gloomy_dreams.agents.retriever import get_news_articles
from gloomy_dreams.agents.summarizer import summarize_article
from gloomy_dreams.agents.sentiment import classify_sentiment

class FinanceState(TypedDict):
    ticker: str
    articles: List[str]
    summaries: List[str]
    sentiments: List[str]

def retrieve_node(state: dict) -> dict:
    articles = get_news_articles(state["ticker"])

    return {**state, "articles": articles}

def summarize_node(state: dict) -> dict:
    summaries = [summarize_article(article) for article in state["articles"]]
    return {**state, "summaries": summaries}

def sentiment_node(state: dict) -> dict:
    sentiments = [classify_sentiment(summary) for summary in state["summaries"]]
    return {**state, "sentiments": sentiments}


def create_finance_graph():
    builder = StateGraph(state_schema=FinanceState)

    # Add nodes explicitly
    builder.add_node("Retrieve News", retrieve_node)
    builder.add_node("Summarize News Content", summarize_node)
    builder.add_node("Calculate Sentiment", sentiment_node)

    # Set the graph structure
    builder.add_edge(START,"Retrieve News")
    builder.add_edge("Retrieve News", "Summarize News Content")
    builder.add_edge("Summarize News Content", "Calculate Sentiment")
    builder.add_edge("Calculate Sentiment",END)


    return builder.compile()
