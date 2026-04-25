# Module 2 — Core Concepts

Understanding MCP requires learning five building blocks: **Servers**, **Clients**, **Tools**, **Resources**, and **Prompts**.

---

## 2.1 Servers

An **MCP server** is a process that exposes capabilities to AI clients. It:

* Runs separately from the AI model (local process, container, or remote service).
* Declares what it can do (tools, resources, prompts) during the *initialisation* handshake.
* Handles requests from the client and returns structured responses.

```
MCP Server responsibilities
├── Respond to initialize / initialized lifecycle messages
├── List available tools, resources, and prompts
└── Execute requests (call a tool, read a resource, expand a prompt)
```

You can build a server in **any language** that can speak JSON-RPC 2.0 over the chosen transport. Official SDKs exist for:

| Language | Package |
|----------|---------|
| TypeScript / Node.js | `@modelcontextprotocol/sdk` |
| Python | `mcp` (PyPI) |
| Kotlin / Java | `io.modelcontextprotocol:kotlin-sdk` |
| C# / .NET | `ModelContextProtocol` (NuGet) |

---

## 2.2 Clients

An **MCP client** is the AI application (or the component inside it) that:

1. Discovers and connects to one or more MCP servers.
2. Forwards the list of tools / resources / prompts to the AI model.
3. Calls the server when the model wants to use a capability.
4. Returns the result to the model.

Well-known MCP clients:

* **Claude Desktop** (Anthropic) — desktop chat with local server support
* **Cursor** — AI code editor
* **Zed** — AI-powered text editor
* **Continue** — VS Code / JetBrains extension
* Any application you build using the MCP SDK

---

## 2.3 Tools

**Tools** are functions the AI model can *invoke*. They are the most commonly used MCP primitive.

```
Tool anatomy
├── name         – unique identifier (e.g. "create_file")
├── description  – plain-English explanation for the AI
├── inputSchema  – JSON Schema describing the expected arguments
└── handler      – your code that executes when the tool is called
```

Example tool definition (conceptual):

```json
{
  "name": "get_weather",
  "description": "Return the current weather for a city.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": { "type": "string", "description": "City name" }
    },
    "required": ["city"]
  }
}
```

When the AI decides to call `get_weather`, MCP routes the call to your server, which fetches real data and returns it.

---

## 2.4 Resources

**Resources** expose *data* that the AI model can read — similar to files or database rows.

```
Resource anatomy
├── uri          – unique address (e.g. "file:///docs/readme.md")
├── name         – human-friendly label
├── mimeType     – content type (text/plain, application/json, …)
└── content      – the actual data (text or binary blob)
```

Resources differ from tools in an important way:
* **Tools** = actions (side-effects possible)
* **Resources** = data (read-only view of state)

Resources can also be **dynamic** (generated on demand) or **static** (pre-defined files).

---

## 2.5 Prompts

**Prompts** are reusable, parameterised message templates the AI (or the user) can invoke to start a well-structured conversation.

```
Prompt anatomy
├── name        – identifier (e.g. "code_review")
├── description – what the prompt does
├── arguments   – optional parameters the caller supplies
└── messages    – the expanded message list returned to the client
```

Example use case: a `summarise_document` prompt that takes a `language` argument and returns a system + user message pair instructing the model to summarise in that language.

---

## 2.6 Transports

MCP is transport-agnostic. The two officially supported transports are:

| Transport | Use case |
|-----------|----------|
| **stdio** | Local servers launched as child processes (most common for desktop tools) |
| **HTTP + SSE** | Remote servers reachable over the network |

Both transports carry the same JSON-RPC 2.0 messages.

---

## 2.7 The Lifecycle

```
Client                          Server
  │                               │
  │──── initialize ──────────────►│
  │◄─── initialize result ────────│  (capabilities exchanged)
  │──── initialized (notify) ────►│
  │                               │
  │──── tools/list ──────────────►│
  │◄─── tools/list result ────────│
  │                               │
  │──── tools/call ──────────────►│  (AI wants to run a tool)
  │◄─── tools/call result ────────│
  │                               │
  │──── shutdown ────────────────►│
```

---

## Summary

| Concept | What It Is | Analogy |
|---------|-----------|---------|
| Server | Process exposing capabilities | A web service |
| Client | AI app consuming capabilities | A browser |
| Tool | Callable function | REST POST endpoint |
| Resource | Readable data | REST GET endpoint |
| Prompt | Message template | Form letter |

---

## Next

➡️ [Module 3 — Environment Setup](../03-setup/README.md)
