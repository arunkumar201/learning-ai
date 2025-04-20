import asyncio

from server import main as start_server


def main():
    print("Starting MCP server...")
    asyncio.run(start_server())


if __name__ == "__main__":
    main()
