import {
	McpServer,
	ResourceTemplate,
} from '@modelcontextprotocol/sdk/server/mcp.js'
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'

import { isBraveLocalSearchArgs, isBraveWebSearchArgs } from '@/api/brave'
import { braveSearchService } from '@/api/brave/service'
import { LOCAL_SEARCH_TOOL } from '@/tools/local-search'
import { WEB_SEARCH_TOOL } from '@/tools/web-search'


export function createMcpServer() {
	const mcpServer = new McpServer(
		{
			name: 'MCP server examples',
			version: '1.0.0',
		},
		{
			capabilities: {
				tools: {
					brave_web_search: WEB_SEARCH_TOOL,
					brave_local_search: LOCAL_SEARCH_TOOL,
				},
			},
		}
	)

	mcpServer.resource(
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

	mcpServer.server.setRequestHandler(ListToolsRequestSchema, async () => ({
		tools: [WEB_SEARCH_TOOL, LOCAL_SEARCH_TOOL],
	}))

	mcpServer.server.setRequestHandler(CallToolRequestSchema, async (request) => {
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
					const { query, count = 10, offset = 0 } = args
					const results = await braveSearchService.performWebSearch(
						query,
						count,
						offset,
						query
					)
					return {
						content: [{ type: 'text', text: results }],
						isError: false,
					}
				}

				case 'brave_local_search': {
					if (!isBraveLocalSearchArgs(args)) {
						throw new Error('Invalid arguments for brave_local_search')
					}
					const { query, count = 4 } = args
					const results = await braveSearchService.performLocalSearch(
						query,
						count,
						query
					)
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
			console.error('Error handling tool call:', error)
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

	return mcpServer
}
