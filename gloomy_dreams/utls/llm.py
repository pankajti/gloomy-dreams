from langchain_ollama.chat_models import ChatOllama

local_llm = None

def get_llm(model_name: str = "mistral") -> ChatOllama:
    """Returns a local Ollama model instance for use with LangChain."""
    global local_llm
    if local_llm is None:
        local_llm= ChatOllama(model=model_name)
    return local_llm

if __name__ == '__main__':
    llm = get_llm()
    resp = llm.invoke("What is your name?")
    print(resp)