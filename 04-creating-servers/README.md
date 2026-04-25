# Module 4 — Creating MCP Servers

In this module you will build your first functional MCP server — a simple **calculator server** — in both TypeScript and Python.

---

## 4.1 Anatomy of an MCP Server

Every MCP server must:

1. Create a `Server` (or `FastMCP`) instance with a name and version.
2. Register its capabilities (tools, resources, prompts).
3. Connect to a transport (stdio for local use).

---

## 4.2 TypeScript: Hello-World Server

Create `src/index.ts`:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 1. Create the server
const server = new McpServer({
  name: "calculator",
  version: "1.0.0",
});

// 2. Register a tool
server.tool(
  "add",
  "Add two numbers together",
  {
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }],
  })
);

server.tool(
  "subtract",
  "Subtract b from a",
  {
    a: z.number().describe("Number to subtract from"),
    b: z.number().describe("Number to subtract"),
  },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a - b) }],
  })
);

// 3. Connect to stdio transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

Install the `zod` validation library (used for input schemas):

```bash
npm install zod
```

Run the server:

```bash
npx tsx src/index.ts
```

---

## 4.3 Python: Hello-World Server

Create `server.py`:

```python
from mcp.server.fastmcp import FastMCP

# 1. Create the server
mcp = FastMCP("calculator")

# 2. Register tools using decorators
@mcp.tool()
def add(a: float, b: float) -> str:
    """Add two numbers together."""
    return str(a + b)

@mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtract b from a."""
    return str(a - b)

# 3. Run with stdio transport (default)
if __name__ == "__main__":
    mcp.run()
```

Run the server:

```bash
python server.py
```

---

## 4.4 Testing with the MCP Inspector

Start the Inspector and connect it to your server:

```bash
# TypeScript
mcp-inspector npx tsx src/index.ts

# Python
mcp-inspector python server.py
```

Open <http://localhost:5173>, then:

1. Click **Connect**.
2. Go to the **Tools** tab — you should see `add` and `subtract`.
3. Click `add`, enter `{ "a": 5, "b": 3 }`, and click **Run Tool**.
4. Observe the result `8`.

---

## 4.5 Server Lifecycle Events

You can hook into lifecycle events to set up and tear down resources:

**TypeScript:**

```typescript
server.server.setRequestHandler(/* initialize */, async (request) => {
  console.error("Server initialised, client:", request.params.clientInfo);
});
```

**Python:**

```python
@mcp.on_event("startup")
async def on_startup():
    print("Server starting up", file=sys.stderr)

@mcp.on_event("shutdown")
async def on_shutdown():
    print("Server shutting down", file=sys.stderr)
```

> **Tip:** Always write debug output to **stderr**, never stdout. Stdout is reserved for the MCP protocol messages when using stdio transport.

---

## 4.6 Error Handling

Return structured errors so the AI client can report them gracefully:

**TypeScript:**

```typescript
server.tool("safe_divide", "Divide a by b", {
  a: z.number(),
  b: z.number(),
}, async ({ a, b }) => {
  if (b === 0) {
    return {
      content: [{ type: "text", text: "Error: division by zero" }],
      isError: true,
    };
  }
  return { content: [{ type: "text", text: String(a / b) }] };
});
```

**Python:**

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

@mcp.tool()
def safe_divide(a: float, b: float) -> str:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return str(a / b)
```

---

## Summary

* An MCP server needs: create → register → connect.
* Use `McpServer` (TypeScript) or `FastMCP` (Python) from the official SDKs.
* Validate inputs with Zod (TypeScript) or Python type annotations.
* Use the MCP Inspector to test without a real AI model.
* Write all debug output to stderr.

---

## Next

➡️ [Module 5 — Working with Tools](../05-tools/README.md)
