# Module 8 — MCP Clients

Once your server is ready, you need to connect it to an **MCP client** — the AI application that will call your tools, read your resources, and use your prompts.

---

## 8.1 Claude Desktop

Claude Desktop is the easiest way to test an MCP server with a real AI model.

### Configuration file location

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

### Adding a local stdio server

```json
{
  "mcpServers": {
    "calculator": {
      "command": "node",
      "args": ["/absolute/path/to/my-mcp-server/dist/index.js"]
    }
  }
}
```

For a Python server:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

For a server that needs environment variables:

```json
{
  "mcpServers": {
    "github-integration": {
      "command": "node",
      "args": ["/path/to/github-server/dist/index.js"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

After saving, **restart Claude Desktop**. A hammer icon (🔨) appears in the chat UI when at least one server is connected successfully.

---

## 8.2 Cursor

Cursor supports MCP via **Settings → Features → MCP**.

1. Open **Cursor Settings** (⌘ + ,).
2. Go to **Features → MCP Servers**.
3. Click **Add New MCP Server**.
4. Enter a name and the command to start your server.

Cursor automatically passes tool definitions to its AI and lets you invoke them in the chat panel.

---

## 8.3 Building a Custom Client (TypeScript)

You can embed an MCP client directly in your own application:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

// 1. Create the transport (launch server as subprocess)
const transport = new StdioClientTransport({
  command: "node",
  args: ["./dist/index.js"],
});

// 2. Create and connect the client
const client = new Client(
  { name: "my-app", version: "1.0.0" },
  { capabilities: { tools: {} } }
);
await client.connect(transport);

// 3. List available tools
const { tools } = await client.listTools();
console.log("Available tools:", tools.map((t) => t.name));

// 4. Call a tool
const result = await client.callTool({ name: "add", arguments: { a: 5, b: 3 } });
console.log("Result:", result.content);

// 5. Clean up
await client.close();
```

---

## 8.4 Building a Custom Client (Python)

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialise
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            # Call a tool
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print("Result:", result.content[0].text)

asyncio.run(main())
```

---

## 8.5 HTTP + SSE Transport (Remote Servers)

For servers accessible over a network, use HTTP with Server-Sent Events (SSE):

**TypeScript server:**

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();
const server = new McpServer({ name: "remote-server", version: "1.0.0" });

// Register tools...

app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/messages", res);
  await server.connect(transport);
});

app.post("/messages", express.json(), async (req, res) => {
  // Handle incoming messages from client
});

app.listen(3000, () => console.error("MCP server listening on port 3000"));
```

**TypeScript client (connecting to remote server):**

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const transport = new SSEClientTransport(new URL("http://localhost:3000/sse"));
const client = new Client({ name: "my-client", version: "1.0.0" }, { capabilities: {} });
await client.connect(transport);
```

---

## 8.6 Debugging Connection Issues

| Symptom | Common cause | Fix |
|---------|-------------|-----|
| Server not listed in Claude Desktop | Config JSON syntax error | Validate JSON at jsonlint.com |
| Server shown but disconnected | Binary not found / wrong path | Use absolute paths; check `command` spelling |
| Tools not appearing | Server crashes on startup | Check stderr output; run server directly in terminal |
| Tool call fails silently | Unhandled exception in handler | Add try/catch; log to stderr |

### Enable debug logging in Claude Desktop

Set the environment variable before launching:

```bash
# macOS
CLAUDE_DEBUG=1 open -a "Claude"
```

---

## Summary

* Claude Desktop and Cursor support MCP out of the box — edit a JSON config file.
* Use the official SDKs to embed an MCP client in your own applications.
* The stdio transport is best for local servers; HTTP + SSE for remote servers.
* Debug by running the server directly in a terminal and checking stderr output.

---

## Next

➡️ [Module 9 — Practical Examples](../09-examples/README.md)
