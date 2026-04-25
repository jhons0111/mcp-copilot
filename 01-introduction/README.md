# Module 1 — Introduction to MCP

## What Is the Model Context Protocol?

The **Model Context Protocol (MCP)** is an open standard developed by Anthropic that defines how AI models communicate with external tools and data sources. Instead of hard-coding integrations inside every AI application, MCP provides a single, well-defined interface that any AI client can use to talk to any MCP server.

```
┌─────────────────┐          MCP           ┌──────────────────────┐
│   AI Client     │ ◄────────────────────► │    MCP Server        │
│  (Claude, etc.) │     (JSON-RPC 2.0)     │  (your integration)  │
└─────────────────┘                        └──────────────────────┘
```

---

## The Problem MCP Solves

Before MCP, connecting an AI model to an external service required:

1. Custom code inside the AI application for every single service.
2. Duplicate effort — every AI product had to re-implement the same integrations.
3. Security risks from ad-hoc, inconsistent designs.

**MCP standardises this bridge.** Build a server once; any MCP-compatible AI client can use it.

---

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Interoperability** | One server works with all MCP-compatible clients |
| **Security** | Servers control what they expose; clients cannot exceed those boundaries |
| **Simplicity** | Small, well-defined surface area (tools, resources, prompts) |
| **Open standard** | MIT-licensed spec anyone can implement |

---

## Real-World Analogy

Think of MCP like **USB**. Before USB, every peripheral (keyboard, mouse, printer) needed its own connector and driver. USB created a single standard. MCP does the same for AI integrations:

* **USB port** = MCP protocol
* **USB device** = MCP server (your integration)
* **Computer** = AI client (Claude Desktop, Cursor, your own app…)

---

## How MCP Fits Into the AI Ecosystem

```
┌──────────────────────────────────────────────────────────────┐
│                        AI Application                        │
│  (Claude Desktop / Cursor / custom chat app / …)             │
│                                                              │
│   ┌──────────┐    MCP    ┌────────────────────────────────┐  │
│   │ AI Model │ ◄───────► │         MCP Host/Client        │  │
│   └──────────┘           └────────────────────────────────┘  │
└──────────────────────────────────────┬───────────────────────┘
                                       │  MCP (stdio / SSE / HTTP)
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
    ┌─────────▼──────┐      ┌──────────▼──────┐      ┌─────────▼──────┐
    │  MCP Server A  │      │  MCP Server B   │      │  MCP Server C  │
    │  (File system) │      │  (GitHub API)   │      │  (Database)    │
    └────────────────┘      └─────────────────┘      └────────────────┘
```

---

## MCP vs. Function Calling / Plugins

| Feature | OpenAI Function Calling | ChatGPT Plugins | **MCP** |
|---------|------------------------|-----------------|---------|
| Standard | Vendor-specific | Vendor-specific | **Open** |
| Works across models | No | No | **Yes** |
| Server reuse | No | Limited | **Yes** |
| Bidirectional updates | No | No | **Yes (resources)** |

---

## What Can You Build with MCP?

* **File-system access** — let the AI read and write your local files
* **Database integrations** — query PostgreSQL, SQLite, MongoDB from a chat
* **API wrappers** — expose GitHub, Jira, Slack, etc.
* **Code execution** — run scripts and return results
* **IoT / device control** — turn on lights, read sensor data
* **Internal tooling** — company wikis, CRMs, deployment pipelines

---

## Summary

* MCP is an open, vendor-neutral protocol for AI ↔ tool communication.
* It separates concerns: the AI client does not need to know implementation details; the server does not need to know which AI model will call it.
* It is built on JSON-RPC 2.0 and supports multiple transports (stdio, HTTP with SSE).

---

## Next

➡️ [Module 2 — Core Concepts](../02-core-concepts/README.md)
