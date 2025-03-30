# multi_client.py
import asyncio
from dotenv import load_dotenv

# Multi MCP 클라이언트 및 에이전트 생성 관련 모듈
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# .env에서 API 키 불러오기
load_dotenv()

# 사용할 OpenAI 모델 초기화
model = ChatOpenAI(model="gpt-4o")

async def main():
    # 여러 MCP 서버의 설정을 구성
    async with MultiServerMCPClient({
        "math": {
            "command": "python",  # 내부적으로 subprocess로 실행
            "args": ["math_server.py"],  # stdio 방식 실행
            "transport": "stdio",
        },
        "naver_api": {
            "url": "http://localhost:8000/sse",  # SSE로 통신
            "transport": "sse",
        }
    }) as client:
        # MCP에서 로드한 tool 목록을 포함하는 LangGraph agent 생성
        agent = create_react_agent(model, client.get_tools())

        # # 1. 수학 질문 → math MCP 사용
        # math_result = await agent.ainvoke({"messages": "what's (4 + 6) x 10?"})
        # print("📐 Math result:\n", math_result)

        # 2. 네이버 블로그 글 검색 질문
        naver_api_result = await agent.ainvoke({"messages": "네이버에서 'MCP'에 대한 블로그 글을 2개만 검색해서 url을 알려줘. 실제로 접속이 되는지 확인해보려고 해."})
        print("🌦️ Access result:\n", naver_api_result)

if __name__ == "__main__":
    asyncio.run(main())
