from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOllama(model="llama3.1")

template = """
Classify the sentiment of the following summary as Positive, Neutral, or Negative:

{text}

Sentiment:
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def classify_sentiment(text: str) -> str:
    result = chain.invoke({"text": text})
    return result.content.strip()
