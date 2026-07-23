import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

# FastMCP 서버 생성
mcp = FastMCP("Cloud-Test-MCP")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """도시 이름을 받아 날씨 정보를 반환합니다."""
    return f"{city}의 현재 날씨는 맑음, 기온은 22도입니다."

# FastAPI 어플리케이션 생성
app = FastAPI(
    title="Open WebUI MCP OpenAPI Wrapper",
    version="1.0.0"
)

# 1. Open WebUI 통신을 위한 CORS 미들웨어 추가 (핵심)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 기본 상태 확인 엔드포인트
@app.get("/")
def read_root():
    return {"status": "ok", "message": "MCP Server is running"}

# 3. Open WebUI OpenAPI 호환 엔드포인트
@app.get("/add_numbers", summary="Add Numbers")
def api_add_numbers(a: int, b: int) -> int:
    """두 정수를 더합니다."""
    return add_numbers(a, b)

@app.get("/get_weather", summary="Get Weather")
def api_get_weather(city: str) -> str:
    """도시 이름을 받아 날씨 정보를 반환합니다."""
    return get_weather(city)

# 4. MCP SSE 앱 마운트
app.mount("/sse", mcp.sse_app())