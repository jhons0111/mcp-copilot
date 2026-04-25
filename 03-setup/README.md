# Module 3 — Environment Setup

This module walks you through installing everything you need to build and test MCP servers in both **Node.js/TypeScript** and **Python**.

---

## 3.1 Prerequisites

| Requirement | Minimum version | Check |
|-------------|----------------|-------|
| Node.js | 18 | `node --version` |
| npm | 9 | `npm --version` |
| Python | 3.10 | `python --version` |
| pip | 23 | `pip --version` |
| Git | 2 | `git --version` |

---

## 3.2 Node.js / TypeScript Setup

### Install Node.js

```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20

# Or download directly from https://nodejs.org
```

### Scaffold a new TypeScript MCP server project

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk
npm install --save-dev typescript @types/node tsx
npx tsc --init
```

Update `tsconfig.json` to target modern Node.js:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "strict": true
  },
  "include": ["src/**/*"]
}
```

Add helpful scripts to `package.json`:

```json
{
  "scripts": {
    "build": "tsc",
    "dev": "tsx watch src/index.ts",
    "start": "node dist/index.js"
  },
  "type": "module"
}
```

### Verify the SDK is available

```bash
node -e "import('@modelcontextprotocol/sdk/server/index.js').then(() => console.log('SDK OK'))"
```

---

## 3.3 Python Setup

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows (PowerShell)
```

### Install the MCP SDK

```bash
pip install mcp
```

### Verify

```bash
python -c "import mcp; print('MCP SDK version:', mcp.__version__)"
```

---

## 3.4 MCP Inspector (optional but recommended)

The **MCP Inspector** is a browser-based developer tool that lets you connect to any MCP server and test its tools, resources, and prompts interactively without needing a full AI client.

```bash
# Install globally
npm install -g @modelcontextprotocol/inspector

# Start the inspector
mcp-inspector
# Opens http://localhost:5173 in your browser
```

---

## 3.5 Claude Desktop (optional)

If you want to test your server with a real AI model, install **Claude Desktop**:

1. Download from <https://claude.ai/download>
2. Open **Settings → Developer → Edit Config** and point it at your server (covered in Module 8).

---

## 3.6 Project Layout Recommendation

For a TypeScript server:

```
my-mcp-server/
├── src/
│   ├── index.ts          ← entry point
│   ├── tools/            ← one file per tool
│   ├── resources/        ← one file per resource provider
│   └── prompts/          ← prompt definitions
├── package.json
├── tsconfig.json
└── README.md
```

For a Python server:

```
my-mcp-server/
├── server.py             ← entry point
├── tools/                ← tool handlers
├── resources/            ← resource handlers
├── prompts/              ← prompt definitions
├── requirements.txt
└── README.md
```

---

## Summary

* Install Node.js ≥ 18 **or** Python ≥ 3.10.
* Add the MCP SDK (`@modelcontextprotocol/sdk` or `mcp`).
* Use the MCP Inspector to test servers during development.

---

## Next

➡️ [Module 4 — Creating MCP Servers](../04-creating-servers/README.md)
