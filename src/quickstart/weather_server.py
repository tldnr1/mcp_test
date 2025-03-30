# weather_server.py
from mcp.server.fastmcp import FastMCP

# MCP 서버 이름 지정
mcp = FastMCP("Weather")

# 비동기 weather tool 정의
@mcp.tool()
async def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny."

# SSE 기반으로 서버 실행
if __name__ == "__main__":
    print(f"Starting Weather MCP server at http://localhost:8000/sse")
    mcp.run(transport="sse")  # localhost:8000/sse에서 SSE 방식으로 대기
