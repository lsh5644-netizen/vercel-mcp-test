import os
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Cloud-Test-MCP")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """도시 이름을 받아 날씨 정보를 반환합니다."""
    return f"{city}의 현재 날씨는 맑음, 기온은 22도입니다."

app = FastAPI()

@app.get("/sse")
async def handle_sse(request):
    async with mcp.sse_server(request) as streams:
        await mcp.run(streams[0], streams[1], mcp.create_initialization_options())