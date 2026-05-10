"""Topic 8 MCP server demo.

Run with stdio transport (for Cursor / Claude Desktop):
    python topics/topic8/mcp_server_demo.py

Run with inspector (recommended while developing):
    mcp dev topics/topic8/mcp_server_demo.py
"""

from mcp.server.fastmcp import FastMCP

from src.financial_analyzer import analyze_company_stub
from src.rag_pipeline import retrieve_stub

mcp = FastMCP("finsight-ai")


@mcp.tool()
def analyze_company(name: str) -> dict:
    """Analyze a company with a rule-based placeholder function.

    Args:
        name: Company name such as "Apple" or "NVIDIA".

    Returns:
        A dictionary with basic analysis fields.
    """
    return analyze_company_stub(name)


@mcp.tool()
def retrieve_docs(query: str, top_k: int = 3) -> list[str]:
    """Retrieve relevant financial text chunks.

    This demo uses `retrieve_stub` from `src.rag_pipeline`.
    Replace the internal call with your real Topic 4 retriever later.

    Args:
        query: Natural-language query from user.
        top_k: Number of chunks to return (default 3).

    Returns:
        A list of retrieved text chunks.
    """
    if top_k <= 0:
        return []
    chunks = retrieve_stub(query)
    return chunks[:top_k]


@mcp.resource("finsight://disclaimer")
def disclaimer() -> str:
    """Provide a reusable financial disclaimer resource."""
    return (
        "本工具仅用于学习与研究目的，不构成任何投资建议。"
        "数据可能过时或不准确，请以官方披露为准。"
    )


if __name__ == "__main__":
    mcp.run()
