import type { Tool } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'


export const WEB_SEARCH_TOOL = {
	name: 'brave_web_search',
	description: `
This tool performs a web search using the Brave Search API, making it ideal for retrieving general information, news, articles, and online content. It's perfect for:

Broad information gathering on a wide range of topics.

Staying updated on recent events or trending topics.

Accessing diverse web sources for comprehensive insights.

Key Features:

Pagination: Supports offsets to navigate through multiple pages of results.

Content Filtering: Allows refining results based on specific criteria.

Freshness Controls: Ensures up-to-date and relevant information.

Usage Notes:

Maximum of 20 results per request.

Use the offset parameter for pagination to retrieve additional results.

This tool is designed to provide accurate, diverse, and timely information from the web, making it a powerful resource for research, fact-checking, and exploration.
`,
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
} satisfies Tool


export const WebSearchParamsSchema = z.object({
	query: z
		.string()
		.min(1)
		.max(400)
		.describe('Search query (max 400 chars, 50 words)'),
	count: z
		.number()
		.min(1)
		.max(20)
		.default(10)
		.describe('Number of results (1-20, default 10)'),
	offset: z
		.number()
		.min(0)
		.max(9)
		.default(0)
		.describe('Pagination offset (max 9, default 0)'),
})


export type WebSearchParams = z.infer<typeof WebSearchParamsSchema>
