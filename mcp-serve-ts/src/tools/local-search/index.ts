import type { Tool } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'


export const LOCAL_SEARCH_TOOL = {
	name: 'brave_local_search',
	description: `
This tool searches for local businesses, places, and services using Brave's Local Search API. It's ideal for queries related to physical locations, such as:

Restaurants, cafes, and bars.

Retail stores, service providers, and businesses.

"Near me" searches or location-specific requests.

Returns Detailed Information:

Business Names and Addresses: Precise locations and contact details.

Ratings and Review Counts: Insights into user feedback and popularity.

Phone Numbers and Opening Hours: Practical details for planning visits.

Key Features:

Automatically falls back to web search if no local results are found.

Perfect for queries that imply proximity or mention specific locations.

Use this tool to find accurate, up-to-date information about nearby businesses and services, making it a valuable resource for location-based inquiries.`,
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
} satisfies Tool


export const LocalSearchParamsSchema = z.object({
	query: z
		.string()
		.min(1)
		.max(400)
		.describe(
			"Local search query (e.g. 'best restaurants near me,hotels near me')"
		),
	count: z
		.number()
		.min(1)
		.max(10)
		.default(4)
		.describe('Number of results (1-10, default 4)'),
})


export type LocalSearchParams = z.infer<typeof LocalSearchParamsSchema>
