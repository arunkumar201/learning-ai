import {
	McpServer,
	ResourceTemplate,
} from '@modelcontextprotocol/sdk/server/mcp.js'
import { z } from 'zod'
import { createSSEServer } from './src/sse-server'

export const ZAddTool = z.object({
	a: z.number({ description: 'this is a number' }),
	b: z.number({ description: 'this is a number' }),
})

const server = new McpServer(
	{
		name: 'MCP Serve TS',
		version: '1.0.0',
	},
	{
		capabilities: {},
	}
)
server.tool('add-two-number', ZAddTool.shape, async ({ a, b }) => {
	console.log('add-two-number tool is called')
	return {
		content: [
			{
				type: 'text',
				text: String(a + b),
			},
		],
	}
})
server.resource(
	'greeting',
	new ResourceTemplate('greeting://{name}', { list: undefined }),
	async (uri, { name }) => ({
		contents: [
			{
				uri: uri.href,
				text: `Hello, ${name}!`,
			},
		],
	})
)
const sseServer = createSSEServer(server)
const PORT = 3001
sseServer.listen(PORT, () => {
	console.log('SSE Server started on port', PORT)
})
