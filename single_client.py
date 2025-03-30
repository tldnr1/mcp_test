# single_client.py
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# .env 파일에서 환경변수를 로드 (예: OPENAI_API_KEY)
load_dotenv()

# 사용할 OpenAI 모델 설정
model = ChatOpenAI(model="gpt-4o")

# math_server.py의 경로를 지정 (절대경로 또는 상대경로)
server_params = StdioServerParameters(
    command="python",
    args=["math_server.py"],  # math_server.py가 현재 폴더에 있다고 가정
)

async def main():
    # stdio_client를 사용하여 math_server와 비동기 연결
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 서버와 연결 초기화
            await session.initialize()
            # math_server에서 제공하는 MCP tool 로딩
            tools = await load_mcp_tools(session)
            # LangGraph 에이전트 생성 (MCP tool이 포함됨)
            agent = create_react_agent(model, tools)
            # 에이전트에게 질의 보내기
            result = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            print(result)

if __name__ == "__main__":
    asyncio.run(main())
