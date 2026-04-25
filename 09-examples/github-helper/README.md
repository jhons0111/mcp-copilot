# Example 3 — GitHub Helper (Python)

An MCP server that integrates with the **GitHub REST API**, letting an AI search repositories and read file contents without leaving the chat.

---

## Features

| Tool | Description |
|------|-------------|
| `search_repositories` | Search GitHub for public repositories by keyword |
| `get_readme` | Fetch the README of a repository |
| `list_files` | List files in a directory of a repository |
| `read_file` | Read the raw content of a file in a repository |

---

## Setup

```bash
cd 09-examples/github-helper

python -m venv .venv
source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

### `requirements.txt`

```
mcp>=1.0.0
httpx>=0.27.0
```

### GitHub Token (optional but recommended)

Without a token, GitHub limits requests to 60/hour. With a token (free tier), you get 5,000/hour.

1. Go to <https://github.com/settings/tokens>.
2. Generate a **classic token** with the `public_repo` scope (or a fine-grained token with read access).
3. Set it as an environment variable:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

---

## Running

```bash
GITHUB_TOKEN=ghp_... mcp-inspector python server.py
```

---

## Claude Desktop Config

```json
{
  "mcpServers": {
    "github-helper": {
      "command": "python",
      "args": ["/absolute/path/to/09-examples/github-helper/server.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

---

## Usage in Claude

> "Search GitHub for MCP server examples."

> "Show me the README of modelcontextprotocol/servers."

> "List the files in the root of the anthropics/courses repository."
