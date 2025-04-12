/* eslint-disable @typescript-eslint/no-explicit-any */
import { z } from 'zod'
import { env } from '@env'

export class BraveApiClient {
	private apiKey: string
	private baseUrl = 'https://api.search.brave.com/res/v1'

	constructor(apiKey = env.BRAVE_API_KEY) {
		this.apiKey = apiKey
	}

	// Web search API
	async webSearch(query: string, count = 10, offset = 0): Promise<any> {
		const url = `${this.baseUrl}/web/search`
		const params = new URLSearchParams({
			q: query,
			count: count.toString(),
			offset: offset.toString(),
		})

		return this.fetchFromBrave(url, params)
	}

	async localSearch(query: string, count = 4): Promise<any> {
		const url = `${this.baseUrl}/local/search`
		const params = new URLSearchParams({
			q: query,
			count: count.toString(),
		})

		return this.fetchFromBrave(url, params)
	}

	private async fetchFromBrave(
		url: string,
		params: URLSearchParams
	): Promise<any> {
		try {
			const response = await fetch(`${url}?${params.toString()}`, {
				headers: {
					Accept: 'application/json',
					'Accept-Encoding': 'gzip',
					'X-Subscription-Token': this.apiKey,
				},
			})

			if (!response.ok) {
				throw new Error(
					`Brave API error: ${response.status} ${response.statusText}`
				)
			}

			return await response.json()
		} catch (error) {
			console.error('Error fetching from Brave API:', error)
			throw error
		}
	}
}

export const BraveWebSearchArgsSchema = z.object({
	query: z.string().min(1).max(400),
	count: z.number().min(1).max(20).default(10),
	offset: z.number().min(0).max(9).default(0),
})

export const BraveLocalSearchArgsSchema = z.object({
	query: z.string().min(1).max(400),
	count: z.number().min(1).max(10).default(4),
})

export function isBraveWebSearchArgs(
	args: any
): args is z.infer<typeof BraveWebSearchArgsSchema> {
	return BraveWebSearchArgsSchema.safeParse(args).success
}

export function isBraveLocalSearchArgs(
	args: any
): args is z.infer<typeof BraveLocalSearchArgsSchema> {
	return BraveLocalSearchArgsSchema.safeParse(args).success
}

export const braveApi = new BraveApiClient()
