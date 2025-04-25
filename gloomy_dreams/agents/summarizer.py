from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

from gloomy_dreams.utls.llm import get_llm
llm = get_llm()


# Template for summarization
template = """
Summarize the following financial news article in 2-3 sentences:

{text}

Summary:
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def summarize_article(text: str) -> str:
    print("summarizing")

    result = chain.invoke({"text": text})

    return result.content.strip()
