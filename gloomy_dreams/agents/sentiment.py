from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from gloomy_dreams.utls.llm import get_llm
llm = get_llm()

template = """
Classify the sentiment of the following summary as Positive, Neutral, or Negative:

{text}

Sentiment:
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def classify_sentiment(text: str) -> str:
    print("Classifying")
    result = chain.invoke({"text": text})
    return result.content.strip()
