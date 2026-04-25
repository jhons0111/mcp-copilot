/**
 * Notes Manager MCP Server
 *
 * Demonstrates tools (create/update/delete) and resources (read notes)
 * in a single server backed by a local JSON file.
 */

import * as fs from "fs/promises";
import * as path from "path";
import { fileURLToPath } from "url";
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// ─── Types ────────────────────────────────────────────────────────────────────

interface Note {
  id: string;
  title: string;
  body: string;
  createdAt: string;
  updatedAt: string;
}

type NotesStore = Record<string, Note>;

// ─── Storage helpers ──────────────────────────────────────────────────────────

const DATA_DIR = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
  "data"
);
const STORE_PATH = path.join(DATA_DIR, "notes.json");

async function readStore(): Promise<NotesStore> {
  try {
    const raw = await fs.readFile(STORE_PATH, "utf-8");
    return JSON.parse(raw) as NotesStore;
  } catch {
    return {};
  }
}

async function writeStore(store: NotesStore): Promise<void> {
  await fs.mkdir(DATA_DIR, { recursive: true });
  await fs.writeFile(STORE_PATH, JSON.stringify(store, null, 2), "utf-8");
}

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

// ─── Server ───────────────────────────────────────────────────────────────────

const server = new McpServer({
  name: "notes-manager",
  version: "1.0.0",
});

// ── Tool: create_note ─────────────────────────────────────────────────────────

server.tool(
  "create_note",
  "Create a new note with a title and body text",
  {
    title: z.string().min(1).describe("Short title for the note"),
    body: z.string().describe("Body / content of the note"),
  },
  async ({ title, body }) => {
    const store = await readStore();
    const id = generateId();
    const now = new Date().toISOString();
    store[id] = { id, title, body, createdAt: now, updatedAt: now };
    await writeStore(store);
    return { content: [{ type: "text", text: `Note created with ID: ${id}` }] };
  }
);

// ── Tool: update_note ─────────────────────────────────────────────────────────

server.tool(
  "update_note",
  "Update the body of an existing note",
  {
    id: z.string().describe("ID of the note to update"),
    body: z.string().describe("New body content"),
  },
  async ({ id, body }) => {
    const store = await readStore();
    if (!store[id]) {
      return {
        content: [{ type: "text", text: `Note not found: ${id}` }],
        isError: true,
      };
    }
    store[id] = { ...store[id], body, updatedAt: new Date().toISOString() };
    await writeStore(store);
    return { content: [{ type: "text", text: `Note ${id} updated.` }] };
  }
);

// ── Tool: delete_note ─────────────────────────────────────────────────────────

server.tool(
  "delete_note",
  "Permanently delete a note by its ID",
  {
    id: z.string().describe("ID of the note to delete"),
  },
  async ({ id }) => {
    const store = await readStore();
    if (!store[id]) {
      return {
        content: [{ type: "text", text: `Note not found: ${id}` }],
        isError: true,
      };
    }
    delete store[id];
    await writeStore(store);
    return { content: [{ type: "text", text: `Note ${id} deleted.` }] };
  }
);

// ── Tool: list_notes ──────────────────────────────────────────────────────────

server.tool(
  "list_notes",
  "Return a list of all note IDs and titles",
  {},
  async () => {
    const store = await readStore();
    const notes = Object.values(store).map(({ id, title, updatedAt }) => ({
      id,
      title,
      updatedAt,
    }));
    return {
      content: [{ type: "text", text: JSON.stringify(notes, null, 2) }],
    };
  }
);

// ── Resource: individual note ─────────────────────────────────────────────────

server.resource(
  "note",
  new ResourceTemplate("note://{id}", { list: undefined }),
  { mimeType: "application/json" },
  async (uri, { id }) => {
    const store = await readStore();
    const note = store[id as string];
    if (!note) {
      throw new Error(`Note not found: ${id}`);
    }
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(note, null, 2),
        },
      ],
    };
  }
);

// ── Resource: notes index ─────────────────────────────────────────────────────

server.resource(
  "notes-index",
  "notes://index",
  { mimeType: "application/json" },
  async () => {
    const store = await readStore();
    const index = Object.values(store).map(({ id, title, updatedAt }) => ({
      id,
      title,
      updatedAt,
    }));
    return {
      contents: [
        {
          uri: "notes://index",
          mimeType: "application/json",
          text: JSON.stringify(index, null, 2),
        },
      ],
    };
  }
);

// ─── Start ────────────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
