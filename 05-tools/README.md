# Module 5 — Working with Tools

Tools are the most powerful MCP primitive. They give AI models the ability to **take actions** — calling APIs, writing files, running queries, and more.

---

## 5.1 Tool Design Principles

| Principle | Guideline |
|-----------|-----------|
| **Single responsibility** | Each tool does one thing well |
| **Descriptive names** | Use verbs: `create_file`, `send_email`, `query_database` |
| **Rich descriptions** | The AI reads your description to decide when to call the tool |
| **Strict schemas** | Validate inputs; reject bad data early |
| **Idempotency** | Where possible, calling the tool twice with the same args should be safe |

---

## 5.2 Input Schema in Depth

The `inputSchema` follows **JSON Schema**. You should always specify:

* `type` for each property
* `description` for each property — the AI uses this to fill arguments correctly
* `required` to prevent missing values
* `enum` for constrained choices

**TypeScript example (Zod):**

```typescript
import { z } from "zod";

server.tool(
  "send_notification",
  "Send a notification to a user via email or SMS",
  {
    userId:  z.string().describe("Target user's ID"),
    channel: z.enum(["email", "sms"]).describe("Delivery channel"),
    message: z.string().min(1).max(500).describe("Notification text"),
    urgent:  z.boolean().optional().default(false).describe("Mark as urgent"),
  },
  async ({ userId, channel, message, urgent }) => {
    // ... implementation
    return { content: [{ type: "text", text: `Notification sent via ${channel}` }] };
  }
);
```

**Python example (type hints + docstring):**

```python
from typing import Literal

@mcp.tool()
def send_notification(
    user_id: str,
    channel: Literal["email", "sms"],
    message: str,
    urgent: bool = False,
) -> str:
    """
    Send a notification to a user via email or SMS.

    Args:
        user_id: Target user's ID.
        channel: Delivery channel — 'email' or 'sms'.
        message: Notification text (max 500 chars).
        urgent: Mark the notification as urgent.
    """
    # ... implementation
    return f"Notification sent via {channel}"
```

---

## 5.3 Returning Rich Content

A tool can return different content types:

```typescript
// Plain text
return { content: [{ type: "text", text: "Hello" }] };

// Multiple items
return {
  content: [
    { type: "text", text: "Here is the chart:" },
    { type: "image", data: base64PngString, mimeType: "image/png" },
  ],
};

// Embedded resource reference
return {
  content: [
    {
      type: "resource",
      resource: { uri: "file:///report.pdf", mimeType: "application/pdf" },
    },
  ],
};
```

---

## 5.4 Async Tools and Long-Running Operations

All tool handlers are async. For long-running operations, return a result as soon as you have it. MCP does not (yet) support streaming tool progress directly, but you can:

1. Start the long operation.
2. Store its state (e.g., job ID in a database).
3. Return a "job started" message immediately.
4. Expose a second `get_job_status` tool for polling.

```typescript
server.tool("start_report", "Start generating a large report", {
  reportType: z.string(),
}, async ({ reportType }) => {
  const jobId = await startReportJob(reportType);
  return { content: [{ type: "text", text: `Job started. ID: ${jobId}` }] };
});

server.tool("get_job_status", "Check the status of a background job", {
  jobId: z.string(),
}, async ({ jobId }) => {
  const status = await checkJobStatus(jobId);
  return { content: [{ type: "text", text: JSON.stringify(status) }] };
});
```

---

## 5.5 Tool Security Considerations

| Risk | Mitigation |
|------|-----------|
| Prompt injection via tool results | Sanitise data before returning; avoid echoing raw user input |
| Destructive operations | Add confirmation parameters or require explicit flags |
| Secrets in schemas | Never put API keys or passwords in tool descriptions |
| Scope creep | Expose only the minimum capabilities needed |

---

## 5.6 Example: File System Tool

**TypeScript:**

```typescript
import * as fs from "fs/promises";
import * as path from "path";

const ALLOWED_DIR = "/tmp/mcp-sandbox";

server.tool(
  "read_file",
  "Read the contents of a file from the sandbox directory",
  { filename: z.string().describe("Name of the file to read") },
  async ({ filename }) => {
    const fullPath = path.join(ALLOWED_DIR, path.basename(filename));
    try {
      const content = await fs.readFile(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    } catch {
      return {
        content: [{ type: "text", text: `File not found: ${filename}` }],
        isError: true,
      };
    }
  }
);
```

---

## 5.7 Exercise

Create a tool called `reverse_string` that:

1. Accepts a single `text` parameter (string, required).
2. Returns the reversed string.
3. Returns an error if the string is empty.

<details>
<summary>Solution (TypeScript)</summary>

```typescript
server.tool(
  "reverse_string",
  "Reverse the characters in a string",
  { text: z.string().min(1).describe("Text to reverse") },
  async ({ text }) => ({
    content: [{ type: "text", text: text.split("").reverse().join("") }],
  })
);
```

</details>

<details>
<summary>Solution (Python)</summary>

```python
@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse the characters in a string."""
    if not text:
        raise ValueError("Text must not be empty")
    return text[::-1]
```

</details>

---

## Summary

* Write clear `description` strings — the AI relies on them.
* Validate all inputs with JSON Schema / Zod / Python type hints.
* Handle errors gracefully and set `isError: true` when appropriate.
* Follow the principle of least privilege — expose only what is needed.

---

## Next

➡️ [Module 6 — Working with Resources](../06-resources/README.md)
