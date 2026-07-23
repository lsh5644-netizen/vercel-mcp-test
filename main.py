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

app = FastAPI(title="MCP-OpenAPI-Wrapper")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MCP Server is running"}

# Open WebUI OpenAPI 호환용 Tool 엔드포인트
@app.get("/add_numbers")
def api_add_numbers(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return add_numbers(a, b)

@app.get("/get_weather")
def api_get_weather(city: str) -> str:
    """도시 이름을 받아 날씨 정보를 반환합니다."""
    return get_weather(city)

app.mount("/sse", mcp.sse_app())