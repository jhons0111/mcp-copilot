import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";


const server = new McpServer({
    name: "Verificador de Contraseñas",
    version: "1.0.0"
});

server.tool(
    "hola",
    "Saluda al usuario con un mensaje de bienvenida",
    { nombre: z.string().describe("Nombre de la persona a saludar") },
    async ({ nombre }) => ({
        content: [{ type: "text", text: `¡Hola, ${nombre}! Bienvenido al servidor MCP.` }]
    })
);

async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

main();