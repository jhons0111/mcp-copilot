# Module 6 — Working with Resources

Resources let your MCP server expose **data** that the AI model can read — similar to files or database rows — without executing code with side-effects.

---

## 6.1 Static Resources

A **static resource** has a fixed URI and content that rarely changes.

**TypeScript:**

```typescript
server.resource(
  "config",
  "app://config/settings",
  { mimeType: "application/json" },
  async () => ({
    contents: [
      {
        uri: "app://config/settings",
        mimeType: "application/json",
        text: JSON.stringify({ theme: "dark", language: "en" }, null, 2),
      },
    ],
  })
);
```

**Python:**

```python
from mcp.types import Resource, TextContent
import json

@mcp.resource("app://config/settings")
def get_config() -> str:
    """Application configuration settings."""
    config = {"theme": "dark", "language": "en"}
    return json.dumps(config, indent=2)
```

---

## 6.2 Dynamic Resources

A **dynamic resource** uses URI templates to serve different data based on parameters in the URL.

**TypeScript:**

```typescript
import { ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";

server.resource(
  "user-profile",
  new ResourceTemplate("users://{userId}/profile", { list: undefined }),
  { mimeType: "application/json" },
  async (uri, { userId }) => {
    const user = await db.users.findById(userId);
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(user, null, 2),
        },
      ],
    };
  }
);
```

**Python:**

```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Fetch a user's profile by ID."""
    user = db.users.find_by_id(user_id)
    return json.dumps(user, indent=2)
```

---

## 6.3 Resource Listing

Clients can request a list of all available resources. You control what appears:

**TypeScript:**

```typescript
// When using `server.resource(...)`, resources are automatically listed.
// For dynamic lists (e.g., files in a directory), you can handle
// resources/list requests manually:
import { ListResourcesRequestSchema } from "@modelcontextprotocol/sdk/types.js";

server.server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const files = await fs.readdir("/data");
  return {
    resources: files.map((f) => ({
      uri: `file:///data/${f}`,
      name: f,
      mimeType: "text/plain",
    })),
  };
});
```

---

## 6.4 Binary Resources

Resources can also contain binary data (images, PDFs, etc.):

```typescript
server.resource(
  "logo",
  "assets://logo.png",
  { mimeType: "image/png" },
  async () => {
    const data = await fs.readFile("./assets/logo.png");
    return {
      contents: [
        {
          uri: "assets://logo.png",
          mimeType: "image/png",
          blob: data.toString("base64"),
        },
      ],
    };
  }
);
```

---

## 6.5 Resource Subscriptions (Push Updates)

MCP supports **resource subscriptions**: when the underlying data changes, the server can notify the client to re-fetch the resource.

```typescript
// Server notifies client that a resource changed
server.server.notification({
  method: "notifications/resources/updated",
  params: { uri: "app://config/settings" },
});
```

The client can then request the updated content. This is useful for live dashboards, file watches, and streaming data.

---

## 6.6 When to Use Resources vs. Tools

| Use case | Resources | Tools |
|----------|-----------|-------|
| Read a config file | ✅ | — |
| Fetch the latest stock price | — | ✅ |
| Browse a catalogue | ✅ | — |
| Submit an order | — | ✅ |
| Read a database row | ✅ | — |
| Update a database row | — | ✅ |

**Rule of thumb:** if the operation only *reads* stable-ish data, use a resource. If it performs an action or requires computation, use a tool.

---

## 6.7 Example: Markdown Documentation Server

A server that exposes all Markdown files in a folder as resources:

```typescript
import * as fs from "fs/promises";
import * as path from "path";

const DOCS_DIR = "./docs";

server.server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const files = await fs.readdir(DOCS_DIR);
  const mdFiles = files.filter((f) => f.endsWith(".md"));
  return {
    resources: mdFiles.map((f) => ({
      uri: `docs://${f}`,
      name: f.replace(".md", ""),
      mimeType: "text/markdown",
    })),
  };
});

server.server.setRequestHandler(ReadResourceRequestSchema, async (req) => {
  const filename = req.params.uri.replace("docs://", "");
  const content = await fs.readFile(path.join(DOCS_DIR, filename), "utf-8");
  return {
    contents: [{ uri: req.params.uri, mimeType: "text/markdown", text: content }],
  };
});
```

---

## 6.8 Exercise

Create a resource at URI `stats://server` that returns a JSON object with:

* `uptime` — number of seconds the server has been running
* `requestCount` — total number of tool/resource calls handled

<details>
<summary>Solution (Python)</summary>

```python
import time
import json

_start_time = time.time()
_request_count = 0

@mcp.resource("stats://server")
def get_server_stats() -> str:
    """Live server statistics."""
    return json.dumps({
        "uptime": round(time.time() - _start_time, 2),
        "requestCount": _request_count,
    })
```

</details>

---

## Summary

* Resources expose read-only data through stable URIs.
* Use static resources for fixed data; dynamic resources (URI templates) for parameterised data.
* Support binary blobs by base64-encoding the content.
* Use resource subscriptions to push updates to interested clients.

---

## Next

➡️ [Module 7 — Prompt Templates](../07-prompts/README.md)
