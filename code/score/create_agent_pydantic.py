import argparse
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()


parser = argparse.ArgumentParser(
    description="Rodar o script com parâmetros configuráveis."
)
parser.add_argument("--provider", type=str, default="ollama")

args = parser.parse_args()
provider = args.provider

if provider == "openai":
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
elif provider == "ollama":
    llm = ChatOllama(temperature=0, model="gemma4:e2b")
else:
    raise ValueError(
        "Provider not supported. Use --provider openai or --provider ollama."
    )

class Source(BaseModel):
    """Schema for a source used by the agent"""

    url:str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and source"""

    answer: str = Field(description="Thr agent's answer to the query")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the answer")


tools = [TavilySearch()]
agent = create_agent(
    model=llm,
    tools=tools,
    response_format=AgentResponse
)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({
        "messages": HumanMessage(content="Search for 3 job postings for an AI engineer using langchain in the bay area on linkedin and list their details")
    })
    print(result)

if __name__ == "__main__":
    main()