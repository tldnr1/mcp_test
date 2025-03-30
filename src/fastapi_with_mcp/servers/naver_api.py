# servers/naver_api.py
import xmltodict
import json
from mcp.server.fastmcp import FastMCP

import os
import httpx

from dotenv import load_dotenv
load_dotenv()


mcp = FastMCP("Naver OpenAPI", dependencies=["httpx", "xmltodict"])


NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")
print(NAVER_CLIENT_ID)
print(NAVER_CLIENT_SECRET)

api_headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
}

API_ENDPOINT = "https://openapi.naver.com/v1"


@mcp.tool(
    name="search_blog",
    description="Search blog posts on Naver",
)
async def search_blog(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search blog posts on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_ENDPOINT}/search/blog.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_news",
    description="Search news articles on Naver",
)
def search_news(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search news articles on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/news.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_book",
    description="Search books on Naver",
)
def search_book(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search books on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/book.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


if __name__ == "__main__":
    print(f"Starting Naver OpenAPI MCP server on port 8000...")
    mcp.run(transport="stdio")
    # mcp.run(transport="sse")
    
    