import { env } from '@env'
import type {
	BraveDescription,
	BravePoiResponse,
	BraveWeb,
} from '../contracts/web-search'
import { rateLimit } from './rate-limit'

export function isBraveWebSearchArgs(
	args: unknown
): args is { query: string; count?: number } {
	return (
		typeof args === 'object' &&
		args !== null &&
		'query' in args &&
		typeof (args as { query: string }).query === 'string'
	)
}

export function isBraveLocalSearchArgs(
	args: unknown
): args is { query: string; count?: number } {
	return (
		typeof args === 'object' &&
		args !== null &&
		'query' in args &&
		typeof (args as { query: string }).query === 'string'
	)
}

async function getPoisData(ids: string[]): Promise<BravePoiResponse> {
	const url = new URL('https://api.search.brave.com/res/v1/local/pois')
	ids.filter(Boolean).forEach((id) => url.searchParams.append('ids', id))
	const response = await fetch(url, {
		headers: {
			Accept: 'application/json',
			'Accept-Encoding': 'gzip',
			'X-Subscription-Token': env.BRAVE_API_KEY,
		},
	})

	if (!response.ok) {
		throw new Error(
			`Brave API error: ${response.status} ${
				response.statusText
			}\n${await response.text()}`
		)
	}

	const poisResponse = (await response.json()) as BravePoiResponse
	return poisResponse
}

async function getDescriptionsData(ids: string[]): Promise<BraveDescription> {
	const url = new URL('https://api.search.brave.com/res/v1/local/descriptions')
	ids.filter(Boolean).forEach((id) => url.searchParams.append('ids', id))
	const response = await fetch(url, {
		headers: {
			Accept: 'application/json',
			'Accept-Encoding': 'gzip',
			'x-subscription-token"': env.BRAVE_API_KEY,
		},
	})

	if (!response.ok) {
		throw new Error(
			`Brave API error: ${response.status} ${
				response.statusText
			}\n${await response.text()}`
		)
	}

	const descriptionsData = (await response.json()) as BraveDescription
	return descriptionsData
}

function formatLocalResults(
	poisData: BravePoiResponse,
	descData: BraveDescription
): string {
	return (
		(poisData.results || [])
			.map((poi) => {
				const address =
					[
						poi.address?.streetAddress ?? '',
						poi.address?.addressLocality ?? '',
						poi.address?.addressRegion ?? '',
						poi.address?.postalCode ?? '',
					]
						.filter((part) => part !== '')
						.join(', ') || 'N/A'

				return `Name: ${poi.name}
Address: ${address}
Phone: ${poi.phone || 'N/A'}
Rating: ${poi.rating?.ratingValue ?? 'N/A'} (${
					poi.rating?.ratingCount ?? 0
				} reviews)
Price Range: ${poi.priceRange || 'N/A'}
Hours: ${(poi.openingHours || []).join(', ') || 'N/A'}
Description: ${descData.descriptions[poi.id] || 'No description available'}
`
			})
			.join('\n---\n') || 'No local results found'
	)
}

export async function performWebSearch(
	query: string,
	count: number = 10,
	offset: number = 0,
	ip: string
) {
	rateLimit(ip)
	const url = new URL('https://api.search.brave.com/res/v1/web/search')
	url.searchParams.set('q', query)
	url.searchParams.set('count', Math.min(count, 20).toString()) // API limit
	url.searchParams.set('offset', offset.toString())

	console.log('Performing web search', url.toString())
	const response = await fetch(url, {
		headers: {
			Accept: 'application/json',
			'Accept-Encoding': 'gzip',
			'X-Subscription-Token': env.BRAVE_API_KEY,
		},
	})

	if (!response.ok) {
		throw new Error(
			`Brave API error: ${response.status} ${
				response.statusText
			}\n${await response.text()}`
		)
	}

	const data = (await response.json()) as BraveWeb

	// Extract just web results
	const results = (data.web?.results || []).map((result) => ({
		title: result.title || '',
		description: result.description || '',
		url: result.url || '',
	}))

	return results
		.map(
			(r) => `Title: ${r.title}\nDescription: ${r.description}\nURL: ${r.url}`
		)
		.join('\n\n')
}

export async function performLocalSearch(
	query: string,
	count: number = 5,
	ip: string
) {
	try {
		await rateLimit(ip)
		// Initial search to get location IDs
		const webUrl = new URL('https://api.search.brave.com/res/v1/web/search')
		webUrl.searchParams.set('q', query)
		webUrl.searchParams.set('search_lang', 'en')
		webUrl.searchParams.set('result_filter', 'locations')
		webUrl.searchParams.set('count', Math.min(count, 20).toString())

		const webResponse = await fetch(webUrl, {
			headers: {
				Accept: 'application/json',
				'Accept-Encoding': 'gzip',
				'X-Subscription-Token': env.BRAVE_API_KEY,
			},
		})

		if (!webResponse.ok) {
			throw new Error(
				`Brave API error: ${webResponse.status} ${
					webResponse.statusText
				}\n${await webResponse.text()}`
			)
		}

		const webData = (await webResponse.json()) as BraveWeb
		const locationIds =
			webData.locations?.results
				?.filter((r): r is { id: string; title?: string } => r.id != null)
				.map((r) => r.id) || []

		if (locationIds.length === 0) {
			return performWebSearch(query, count, undefined, ip) // Fallback to web search
		}

		// Get POI details and descriptions in parallel
		const [poisData, descriptionsData] = await Promise.all([
			getPoisData(locationIds),
			getDescriptionsData(locationIds),
		])

		return formatLocalResults(poisData, descriptionsData)
	} catch (e) {
		console.error(e)
		throw new Error('Error performing local search')
	}
}
