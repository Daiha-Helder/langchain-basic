import argparse
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

tavily =  TavilyClient()
parser = argparse.ArgumentParser(
    description="Rodar o script com parâmetros configuráveis."
)
parser.add_argument("--provider", type=str)

args = parser.parse_args()
provider = args.provider

@tool
def search(query: str) -> str:
    """
    Tool that searches over internet 
    Args:
        query: The query to search for 
    Returns:
        The search result
    """
    print(f"Searching for {query}")
    return tavily.search(query=query)


if provider == "openai":
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
elif provider == "ollama":
    llm = ChatOllama(temperature=0, model="gemma4:e2b")
else:
    raise ValueError(
        "Provider not supported. Use --provider openai or --provider ollama."
    )

tools = [search]
agent = create_agent(
    model=llm,
    tools=tools
)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({
        "messages": HumanMessage(content="Search for 3 job postings for an AI engineer using langchain in the bay area on linkedin and list their details")
    })
    print(result)

if __name__ == "__main__":
    main()