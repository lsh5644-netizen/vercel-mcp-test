import os
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# FastMCP 서버 인스턴스 생성
mcp = FastMCP("Cloud-Test-MCP")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """도시 이름을 받아 날씨 정보를 반환합니다."""
    return f"{city}의 현재 날씨는 맑음, 기온은 22도입니다."

# FastAPI 앱 생성 및 FastMCP의 sse_app을 마운트/연결
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MCP Server is running"}

# mcp 객체에서 지원하는 sse_app을 엔드포인트로 노출
app.mount("/sse", mcp.sse_app())