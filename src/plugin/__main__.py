"""MCP server for the synthetic filing corpus."""

from __future__ import annotations

from typing import Any

import anyio
from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from slimconfig import build_output, output_schema, plain_output

from contract import TOOLS, Tool
from plugin import list_filings, read_filing

server = Server("financial-filing-fact-retriever")
IMPLEMENTATIONS = {Tool.LIST_FILINGS: list_filings, Tool.READ_FILING: read_filing}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=tool.value, inputSchema=output_schema(given), outputSchema=output_schema(made))
        for tool, (given, made) in TOOLS.items()
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    tool = Tool(name)
    given, made = TOOLS[tool]
    output = IMPLEMENTATIONS[tool](build_output(arguments, given))
    if not isinstance(output, made):
        raise TypeError(f"{name} returned {type(output).__name__}, not {made.__name__}")
    return plain_output(output)


def main() -> None:
    if set(IMPLEMENTATIONS) != set(Tool):
        raise SystemExit("IMPLEMENTATIONS must implement every contract.Tool")

    async def run() -> None:
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    anyio.run(run)


if __name__ == "__main__":
    main()
