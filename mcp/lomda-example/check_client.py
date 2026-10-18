"""Smoke test: start server.py over stdio and call every capability."""
import asyncio
import pathlib
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

HERE = pathlib.Path(__file__).parent


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()
            print("tools:", [t.name for t in tools.tools])
            res = await s.call_tool("list_tasks", {"status": "open"})
            print("list_tasks(open):", res.content[0].text)
            bad = await s.call_tool("list_tasks", {"status": "later"})
            print("list_tasks(later):", getattr(bad, "is_error", None), bad.content[0].text)
            rs = await s.list_resources()
            print("resources:", [str(x.uri) for x in rs.resources])
            rd = await s.read_resource("tasks://summary")
            print("summary:", rd.contents[0].text)
            ps = await s.list_prompts()
            print("prompts:", [p.name for p in ps.prompts])


asyncio.run(main())
