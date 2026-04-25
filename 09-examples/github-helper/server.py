"""
GitHub Helper MCP Server
Provides tools to search repositories and read file contents via the GitHub REST API.
"""

import base64
import json
import os
import sys
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("github-helper")

# ─── GitHub API client ────────────────────────────────────────────────────────

GITHUB_API = "https://api.github.com"
_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def _headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if _TOKEN:
        headers["Authorization"] = f"Bearer {_TOKEN}"
    return headers


async def _get(path: str, params: Optional[dict] = None) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{GITHUB_API}{path}", headers=_headers(), params=params)
        resp.raise_for_status()
        return resp.json()


# ─── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
async def search_repositories(query: str, max_results: int = 5) -> str:
    """
    Search GitHub for public repositories matching a keyword query.

    Args:
        query:       Search keywords (e.g. 'mcp server python').
        max_results: Maximum number of results to return (1–20, default 5).
    """
    if not 1 <= max_results <= 20:
        return "Error: max_results must be between 1 and 20"

    try:
        data = await _get("/search/repositories", {"q": query, "per_page": max_results, "sort": "stars"})
        items = [
            {
                "full_name": r["full_name"],
                "description": r.get("description", ""),
                "stars": r["stargazers_count"],
                "url": r["html_url"],
                "language": r.get("language"),
            }
            for r in data.get("items", [])
        ]
        return json.dumps(items, indent=2)
    except httpx.HTTPStatusError as exc:
        return f"GitHub API error: {exc.response.status_code} {exc.response.text}"


@mcp.tool()
async def get_readme(owner: str, repo: str) -> str:
    """
    Fetch the README of a GitHub repository.

    Args:
        owner: Repository owner or organisation (e.g. 'modelcontextprotocol').
        repo:  Repository name (e.g. 'servers').
    """
    try:
        data = await _get(f"/repos/{owner}/{repo}/readme")
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        return content
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return f"README not found for {owner}/{repo}"
        return f"GitHub API error: {exc.response.status_code}"


@mcp.tool()
async def list_files(owner: str, repo: str, path: str = "") -> str:
    """
    List files and directories in a repository path.

    Args:
        owner: Repository owner.
        repo:  Repository name.
        path:  Path within the repository (empty string = root).
    """
    try:
        data = await _get(f"/repos/{owner}/{repo}/contents/{path}")
        if isinstance(data, dict):
            return f"Error: {path!r} is a file, not a directory"
        items = [
            {"name": item["name"], "type": item["type"], "size": item.get("size", 0)}
            for item in data
        ]
        return json.dumps(items, indent=2)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return f"Path not found: {owner}/{repo}/{path}"
        return f"GitHub API error: {exc.response.status_code}"


@mcp.tool()
async def read_file(owner: str, repo: str, path: str) -> str:
    """
    Read the raw text content of a file in a GitHub repository.

    Args:
        owner: Repository owner.
        repo:  Repository name.
        path:  File path within the repository (e.g. 'src/main.py').
    """
    try:
        data = await _get(f"/repos/{owner}/{repo}/contents/{path}")
        if isinstance(data, list):
            return f"Error: {path!r} is a directory, not a file"
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        return content
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return f"File not found: {owner}/{repo}/{path}"
        return f"GitHub API error: {exc.response.status_code}"


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
