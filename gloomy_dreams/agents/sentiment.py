from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from gloomy_dreams.utls.llm import get_llm
llm = get_llm()

template = """
Classify the sentiment of the following summary as Positive, Neutral, or Negative no other explanations please:

{text}

Sentiment:
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def classify_sentiment(text: str) -> str:
    print("Classifying")
    result = chain.invoke({"text": text})
    if isinstance(result,str):
        ai_result = result
    else:
        ai_result= result.content
    return ai_result.strip()
