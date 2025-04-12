import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js'
import express,{ type Request,type Response } from 'express'

const transportMap = new Map<string,SSEServerTransport>()

export interface SseConfig {
	path: string
	corsOrigins: string
}

export function createSSEServer(mcpServer: McpServer,config: SseConfig) {
	const app = express()

	app.use((req,res,next) => {
		res.setHeader('Access-Control-Allow-Origin',config.corsOrigins)
		res.setHeader('Access-Control-Allow-Methods','GET, POST, OPTIONS')
		res.setHeader('Access-Control-Allow-Headers','Content-Type')

		if (req.method === 'OPTIONS') {
			res.status(204).end()
			return
		}

		next()
	})

	app.get(config.path || '/sse',async (req,res) => {
		try {
			res.setHeader('Content-Type','text/event-stream')
			res.setHeader('Cache-Control','no-cache')
			res.setHeader('Connection','keep-alive')

			const transport = new SSEServerTransport('/messages',res)
			transportMap.set(transport.sessionId,transport)

			await mcpServer.connect(transport)

			req.on('close',() => {
				transportMap.delete(transport.sessionId)
				console.log('Client disconnected:',transport.sessionId)
			})

			res.write(
				`data: ${JSON.stringify({
					type: 'connected',
					sessionId: transport.sessionId,
				})}\n\n`
			)
		} catch (error) {
			console.error('Error connecting to MCP server:',error)
			if (!res.headersSent) {
				res.status(500).send('Error connecting to MCP server')
			}
		}
	})
	// eslint-disable-next-line @typescript-eslint/ban-ts-comment
	//@ts-ignore
	app.post('/messages',(req: Request,res: Response) => {
		const sessionId = req.query.sessionId?.toString()
		if (!sessionId) {
			return res.status(400).send('Session ID is required')
		}

		const transport = transportMap.get(sessionId)
		if (!transport) {
			return res.status(404).send('Transport not found')
		}

		try {
			return transport.handlePostMessage(req,res)
		} catch (error) {
			console.error('Error handling message:',error)
			if (!res.headersSent) {
				res.status(500).send('Error handling message')
			}
		}
	})

	app.get('/health',(_,res) => {
		res.status(200).send({ status: 'ok' })
	})

	return app
}
