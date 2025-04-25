import httpx
import os
from newspaper import Article

from dotenv import load_dotenv
env_path = '/Users/pankajti/dev/git/gloomy-dreams/gloomy_dreams/config/.env'
if os.path.exists(env_path):
    load_dotenv(env_path)


def get_full_article_text(url: str) -> str:
    """Download and extract full article text from the given URL."""
    print(f"downloading {url}")
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        print(f"[ERROR] Failed to extract from {url}: {e}")
        return ""  # fallback to empty if scraping fails

def get_news_articles(ticker: str, max_results: int = 3) -> list[dict]:
    """Fetch top news articles and return full text + title for each."""
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise RuntimeError("Missing NEWSAPI_KEY in environment.")

    url = (
        f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt"
        f"&pageSize={max_results}&apiKey={api_key}"
    )

    response = httpx.get(url)
    if response.status_code != 200:
        print(f"[ERROR] NewsAPI failed: {response.status_code}")
        return []

    results = []
    for article in response.json().get("articles", []):
        title = article["title"]
        article_url = article["url"]
        text = get_full_article_text(article_url)

        # Only keep articles that were successfully parsed
        if text:
            results.append({
                "title": title,
                "text": text,
                "url": article_url,
            })

    return results
