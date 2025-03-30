# agents/graph.py
from contextlib import asynccontextmanager
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langsmith import traceable
from langchain_mcp_adapters.client import MultiServerMCPClient

from dotenv import load_dotenv
load_dotenv()

@traceable(name="fastapi_with_mcp")
@asynccontextmanager
async def make_graph():
    model = ChatOpenAI(model="gpt-4o")  # LangSmith가 자동 추적
    async with MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["servers/math_server.py"],
            "transport": "stdio"
        },
        "naver_api": {
            "command": "python",
            "args": ["servers/naver_api.py"],
            "transport": "stdio" # "sse"
        }
    }) as client:
        agent = create_react_agent(model, client.get_tools())
        yield agent
