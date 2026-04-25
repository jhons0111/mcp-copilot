# Example 2 — Notes Manager (TypeScript)

A CRUD MCP server for managing plain-text notes stored in a local JSON file. This example demonstrates tools for writing data **and** resources for reading it.

---

## Features

| Tool | Description |
|------|-------------|
| `create_note` | Create a new note with a title and body |
| `update_note` | Update the body of an existing note |
| `delete_note` | Delete a note by ID |
| `list_notes` | List all note titles and IDs |

| Resource | URI | Description |
|----------|-----|-------------|
| Note | `note://{id}` | Full content of a note |
| Index | `notes://index` | JSON list of all notes |

---

## Setup

```bash
cd 09-examples/notes-manager
npm install
npm run build
```

### `package.json` dependencies

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0"
  }
}
```

---

## Running

```bash
# Development (auto-reload)
npm run dev

# With MCP Inspector
mcp-inspector npm run dev

# Production
npm run build && npm start
```

---

## Claude Desktop Config

```json
{
  "mcpServers": {
    "notes": {
      "command": "node",
      "args": ["/absolute/path/to/09-examples/notes-manager/dist/index.js"]
    }
  }
}
```

---

## Usage in Claude

> "Create a note called 'Shopping list' with milk, eggs, and bread."

> "Show me my shopping list note."

> "Add bananas to the shopping list note."

> "Delete the shopping list note."
