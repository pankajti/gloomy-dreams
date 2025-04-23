from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize the model
llm = ChatOllama(model="llama3.1")

# Template for summarization
template = """
Summarize the following financial news article in 2-3 sentences:

{text}

Summary:
"""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm


def summarize_article(text: str) -> str:
    result = chain.invoke({"text": text})

    return result.content.strip()
