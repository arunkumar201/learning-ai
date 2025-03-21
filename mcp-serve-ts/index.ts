import {
	McpServer,
	ResourceTemplate,
} from '@modelcontextprotocol/sdk/server/mcp.js'
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'
import { LOCAL_SEARCH_TOOL_DESCRIPTION } from './src/constants/web-search'
import {
	isBraveLocalSearchArgs,
	isBraveWebSearchArgs,
	performLocalSearch,
	performWebSearch,
} from './src/helper/web-search'
import { createSSEServer } from './src/sse-server'
import { WEB_SEARCH_TOOL } from './src/tools/web-search'

export const ZAddTool = z.object({
	a: z.number({ description: 'this is a number' }),
	b: z.number({ description: 'this is a number' }),
})

export const mcp_server = new McpServer(
	{
		name: 'MCP Serve TS',
		version: '1.0.0',
	},
	{
		capabilities: {
			tools: {},
		},
	}
)
mcp_server.tool('add-two-number', ZAddTool.shape, async ({ a, b }) => {
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
mcp_server.resource(
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

mcp_server.server.setRequestHandler(ListToolsRequestSchema, async () => ({
	tools: [WEB_SEARCH_TOOL, LOCAL_SEARCH_TOOL_DESCRIPTION],
}))

mcp_server.server.setRequestHandler(CallToolRequestSchema, async (request) => {
	try {
		const { name, arguments: args } = request.params

		if (!args) {
			throw new Error('No arguments provided')
		}

		switch (name) {
			case 'brave_web_search': {
				if (!isBraveWebSearchArgs(args)) {
					throw new Error('Invalid arguments for brave_web_search')
				}
				const { query, count = 10 } = args
				const results = await performWebSearch(query, count, undefined, query)
				return {
					content: [{ type: 'text', text: results }],
					isError: false,
				}
			}

			case 'brave_local_search': {
				if (!isBraveLocalSearchArgs(args)) {
					throw new Error('Invalid arguments for brave_local_search')
				}
				const { query, count = 5 } = args
				const results = await performLocalSearch(query, count, query)
				return {
					content: [{ type: 'text', text: results }],
					isError: false,
				}
			}

			default:
				return {
					content: [{ type: 'text', text: `Unknown tool: ${name}` }],
					isError: true,
				}
		}
	} catch (error) {
		return {
			content: [
				{
					type: 'text',
					text: `Error: ${
						error instanceof Error ? error.message : String(error)
					}`,
				},
			],
			isError: true,
		}
	}
})

const sseServer = createSSEServer(mcp_server)
const PORT = 3001
sseServer.listen(PORT, () => {
	console.log('SSE Server started on port', PORT)
})
