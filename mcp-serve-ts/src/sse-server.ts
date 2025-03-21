import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js'
import express from 'express'

const transportMap = new Map<string, SSEServerTransport>()

const app = express()

export function createSSEServer(mcpServer: McpServer) {
	app.get('/sse', async (req, res) => {
		try {
			const transport = new SSEServerTransport('/messages', res)
			transportMap.set(transport.sessionId, transport)
			await mcpServer.connect(transport)
		} catch (error) {
			console.error('Error connecting to MCP server:', error)
			res.status(500).send('Error connecting to MCP server')
			return
		}
	})

	app.post('/messages', (req, res) => {
		const sessionId = req.query.sessionId?.toString() ?? '12'
		console.log('Message received', sessionId)
		if (!sessionId) {
			console.error('Message received without sessionId')
			res.status(400).json({ error: 'sessionId is required' })
			return
		}

		const transport = transportMap.get(sessionId)

		if (transport) {
			return transport.handlePostMessage(req, res)
		}
	})

	app.get('/hello', (_req, res) => {
		res.send('Hello World')
	})

	return app
}
