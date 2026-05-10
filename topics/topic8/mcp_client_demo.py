"""Topic 8 MCP Python client demo.

Use this file to verify `mcp_server_demo.py` without Cursor/Claude.
Run from repository root:
    python topics/topic8/mcp_client_demo.py
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    params = StdioServerParameters(
        command="python",
        args=["topics/topic8/mcp_server_demo.py"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [tool.name for tool in tools.tools])

            result = await session.call_tool("analyze_company", {"name": "Apple"})
            print("Result:", result.content)


if __name__ == "__main__":
    asyncio.run(main())
