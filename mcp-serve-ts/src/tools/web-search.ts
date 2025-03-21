import type { Tool } from '@modelcontextprotocol/sdk/types.js'
import {
	LOCAL_SEARCH_TOOL_DESCRIPTION,
	WEB_SEARCH_TOOL_DESCRIPTION,
} from '../constants/web-search'

export const WEB_SEARCH_TOOL: Tool = {
	name: 'brave_web_search',
	description: WEB_SEARCH_TOOL_DESCRIPTION,
	inputSchema: {
		type: 'object',
		properties: {
			query: {
				type: 'string',
				description: 'Search query (max 400 chars, 50 words)',
			},
			count: {
				type: 'number',
				description: 'Number of results (1-20, default 10)',
				default: 10,
			},
			offset: {
				type: 'number',
				description: 'Pagination offset (max 9, default 0)',
				default: 0,
			},
		},
		required: ['query'],
	},
}

export const LOCAL_SEARCH_TOOL: Tool = {
	name: 'brave_local_search',
	description: LOCAL_SEARCH_TOOL_DESCRIPTION,
	inputSchema: {
		type: 'object',
		properties: {
			query: {
				type: 'string',
				description:
					"Local search query (e.g. 'best restaurants near me,hotels near me')",
			},
			count: {
				type: 'number',
				description: 'Number of results (1-10, default 4)',
				default: 4,
			},
		},
		required: ['query'],
	},
}
