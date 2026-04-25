# Module 7 — Prompt Templates

**Prompts** are reusable, parameterised conversation starters that MCP servers can expose. Users (or AI orchestrators) invoke a prompt by name to receive a ready-made message list.

---

## 7.1 When to Use Prompts

* Standardise repetitive tasks ("Review this code", "Summarise this document").
* Enforce consistent instructions across teams and projects.
* Let non-developers customise AI behaviour without editing system prompts.
* Provide AI-assisted workflows that always begin with the right context.

---

## 7.2 Defining a Simple Prompt

**TypeScript:**

```typescript
server.prompt(
  "summarise",
  "Summarise a piece of text",
  {
    text: z.string().describe("The text to summarise"),
  },
  ({ text }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Please provide a concise summary of the following text:\n\n${text}`,
        },
      },
    ],
  })
);
```

**Python:**

```python
from mcp.types import GetPromptResult, PromptMessage, TextContent

@mcp.prompt()
def summarise(text: str) -> str:
    """
    Summarise a piece of text.

    Args:
        text: The text to summarise.
    """
    return f"Please provide a concise summary of the following text:\n\n{text}"
```

---

## 7.3 Multi-Turn Prompts

Prompts can include multiple messages to set up a conversation with history:

```typescript
server.prompt(
  "code_review",
  "Request a code review with context",
  {
    language: z.string().describe("Programming language"),
    code:     z.string().describe("The code to review"),
  },
  ({ language, code }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: [
            `You are an expert ${language} developer.`,
            "Review the following code for correctness, performance, and style.",
            "Provide specific, actionable feedback.",
          ].join(" "),
        },
      },
      {
        role: "user",
        content: {
          type: "text",
          text: `\`\`\`${language}\n${code}\n\`\`\``,
        },
      },
    ],
  })
);
```

---

## 7.4 Prompts with Resource References

Prompts can reference resources, letting the AI load data automatically:

```typescript
server.prompt(
  "analyse_document",
  "Analyse a document stored as an MCP resource",
  {
    documentUri: z.string().describe("URI of the document resource"),
  },
  ({ documentUri }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: "Please analyse the following document and identify key insights:",
        },
      },
      {
        role: "user",
        content: {
          type: "resource",
          resource: { uri: documentUri, mimeType: "text/plain" },
        },
      },
    ],
  })
);
```

---

## 7.5 Listing and Getting Prompts

Clients call `prompts/list` to discover available prompts and `prompts/get` to expand one with arguments.

Example response from `prompts/list`:

```json
{
  "prompts": [
    {
      "name": "summarise",
      "description": "Summarise a piece of text",
      "arguments": [
        { "name": "text", "description": "The text to summarise", "required": true }
      ]
    }
  ]
}
```

---

## 7.6 Prompt Best Practices

| Practice | Reason |
|----------|--------|
| Use clear, imperative descriptions | Helps users and orchestrators pick the right prompt |
| Keep prompts focused | One task per prompt |
| Document all arguments | Clients display these to users |
| Avoid hard-coded secrets | Prompts are visible to clients |
| Test with real AI models | Verify the prompt produces the desired behaviour |

---

## 7.7 Example: Multilingual Greeting Generator

```python
from typing import Literal

@mcp.prompt()
def greeting_generator(
    name: str,
    language: Literal["English", "Spanish", "French", "Portuguese"] = "English",
) -> str:
    """
    Generate a personalised greeting in the specified language.

    Args:
        name: The person's name.
        language: Target language for the greeting.
    """
    return (
        f"Generate a warm, personalised greeting for someone named '{name}'. "
        f"Write the greeting in {language}. "
        "Keep it friendly and professional."
    )
```

---

## 7.8 Exercise

Create a prompt called `bug_report` that:

* Accepts `title` (required) and `description` (optional) parameters.
* Returns a message asking the AI to produce a well-structured bug report.

<details>
<summary>Solution (TypeScript)</summary>

```typescript
server.prompt(
  "bug_report",
  "Generate a structured bug report",
  {
    title:       z.string().describe("Short title of the bug"),
    description: z.string().optional().describe("Additional context"),
  },
  ({ title, description }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: [
            `Create a well-structured bug report for the following issue: "${title}".`,
            description ? `Additional context: ${description}` : "",
            "Include sections for: Summary, Steps to Reproduce, Expected Behaviour, Actual Behaviour, and Suggested Fix.",
          ].filter(Boolean).join(" "),
        },
      },
    ],
  })
);
```

</details>

---

## Summary

* Prompts are parameterised message templates registered on the server.
* They support single-turn and multi-turn conversations.
* They can embed resource references to inject data automatically.
* Clients discover them via `prompts/list` and expand them via `prompts/get`.

---

## Next

➡️ [Module 8 — MCP Clients](../08-clients/README.md)
