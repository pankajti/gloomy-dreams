import httpx
import os

from dotenv import load_dotenv
env_path = '/Users/pankajti/dev/git/gloomy-dreams/gloomy_dreams/config/.env'
if os.path.exists(env_path):
    load_dotenv(env_path)

def get_news_articles(ticker: str, max_results: int = 3) -> list:
    """Fetch top financial news articles using NewsAPI (or mock data)."""
    api_key = os.getenv("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&pageSize={max_results}&apiKey={api_key}"

    response = httpx.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    return [article["title"] for article in data.get("articles", [])]
