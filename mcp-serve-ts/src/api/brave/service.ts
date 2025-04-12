import { createRateLimiter } from '@/utils/rate-limiter'
import { formatLocalSearchResults, formatWebSearchResults } from './formatters'
import { braveApi } from './index'

const webSearchLimiter = createRateLimiter({
	tokensPerInterval: 10,
	interval: 'minute',
})
const localSearchLimiter = createRateLimiter({
	tokensPerInterval: 10,
	interval: 'minute',
})

export class BraveSearchService {
	async performWebSearch(
		query: string,
		count = 10,
		offset = 0,
		originalQuery?: string
	): Promise<string> {
		await webSearchLimiter.consume()

		try {
			const data = await braveApi.webSearch(query, count, offset)
			return formatWebSearchResults(data, originalQuery || query)
		} catch (error) {
			console.error('Web search error:', error)
			return `Error performing web search: ${
				error instanceof Error ? error.message : String(error)
			}`
		}
	}

	async performLocalSearch(
		query: string,
		count = 4,
		originalQuery?: string
	): Promise<string> {
		await localSearchLimiter.consume()

		try {
			const data = await braveApi.localSearch(query, count)
			return formatLocalSearchResults(data, originalQuery || query)
		} catch (error) {
			console.error('Local search error:', error)
			return `Error performing local search: ${
				error instanceof Error ? error.message : String(error)
			}`
		}
	}
}

export const braveSearchService = new BraveSearchService()
