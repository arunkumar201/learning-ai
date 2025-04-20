# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("learning-mcp")

@mcp.tool()
def add(a: int, b: int) -> int:
    print(f"Adding {a} and {b}")
    return a + b


@mcp.prompt()
def get_prompt(a: int, b: int) -> str:
    return f"What is {a} + {b}?"


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"


# start the fastmcp sse server
def start_server():
    mcp.run_sse_async()
