from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def dummy_tool(x: str) -> str:
    """A dummy tool"""
    return "dummy"

chat = ChatOpenAI(model="minimax/minimax-m2.5:free", openai_api_key="sk-or-v1-dummy", openai_api_base="https://openrouter.ai/api/v1")
agent = create_agent(chat, tools=[dummy_tool], system_prompt="You are a dummy.")
res = agent.invoke({"messages": [{"role": "user", "content": "hi"}]})
print(res)
