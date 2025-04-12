# MCP Server in TypeScript

A robust server implementation of the Model Context Protocol (MCP) with Server-Sent Events (SSE) support, featuring Brave Search API integration for web and local search capabilities and scalable Project Architecture.

## Features

- **MCP Protocol Support**: Implements the [Model Context Protocol](https://github.com/modecry/modelcontextprotocol) for AI tool integration
- **SSE Integration**: Real-time communication using Server-Sent Events
- **Brave Search API**: Web search and local business search functionality
- **Rate Limiting**: Built-in protection against API abuse
- **TypeScript**: Type-safe implementation with Zod validation

## Environment Variables

The server is configured using environment variables. Create a `.env` file in the root directory based on the provided `.env.example`.

### Required Environment Variables
 - PORT -  The port the server will listen on | 3001 /n
 - NODE_ENV - The environment mode (development, production, test) | development /n
 - SSE_ENDPOINT - The endpoint for SSE connections | /sse /n
 - BRAVE_API_KEY - Brave API key for web search (required)

## Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and add your Brave API key:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   pnpm install
   # or

   bun install
   ```

## Usage

### Starting the Server

```bash
# Prod mode
pnpm start
# or
bun run start
```

### Dev  Mode
```bash
pnpm dev
# or
bun run dev
```

This will start both the MCP inspector and the server for easier debugging.

## MCP Tools Available 
-  http://localhost:6274

## MCP Client Configuration

To connect to this server from an MCP client, use the following configuration:

```json
{
  "mcpServers": {
    "server-name": {
      "url": "http://localhost:3001/sse",
      "timeout": 10000
    }
  }
}
```
