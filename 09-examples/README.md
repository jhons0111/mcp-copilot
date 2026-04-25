# Module 9 — Practical Examples

This module contains three fully working, end-to-end examples that tie together everything from the previous modules.

---

## Example List

| # | Name | Language | Description |
|---|------|----------|-------------|
| 1 | [Weather Server](weather-server/) | Python | Fetch current weather via a public API |
| 2 | [Notes Manager](notes-manager/) | TypeScript | CRUD for local text notes |
| 3 | [GitHub Helper](github-helper/) | Python | Search repositories and read file contents |

Each example folder contains:
* `README.md` — setup and usage instructions
* Source code ready to run
* Instructions for connecting to Claude Desktop

---

## How to Run Any Example

1. Navigate into the example directory.
2. Install dependencies (see each example's README).
3. Test with the MCP Inspector:
   ```bash
   # TypeScript
   mcp-inspector npx tsx src/index.ts

   # Python
   mcp-inspector python server.py
   ```
4. Connect to Claude Desktop by adding the server to `claude_desktop_config.json`.

---

## Next Steps

After completing these examples, explore:

* **Official MCP servers** — <https://github.com/modelcontextprotocol/servers>
* **MCP specification** — <https://spec.modelcontextprotocol.io>
* **Community servers** — search GitHub for `topic:mcp-server`
* **Building production servers** — add authentication, rate limiting, and monitoring
