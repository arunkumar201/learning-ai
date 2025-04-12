/* eslint-disable @typescript-eslint/no-explicit-any */

export function formatWebSearchResults(
	data: any,
	originalQuery: string
): string {
	if (!data || !data.web || !data.web.results) {
		return 'No results found.'
	}

	const { results } = data.web
	const formattedResults = results
		.map((result: any, index: number) => {
			return `[${index + 1}] ${result.title}\n${
				result.description || 'No description available.'
			}\nURL: ${result.url}\n`
		})
		.join('\n')

	return `Search results for: "${originalQuery}"\n\n${formattedResults}`
}

export function formatLocalSearchResults(
	data: any,
	originalQuery: string
): string {
	if (
		!data ||
		!data.local ||
		!data.local.results ||
		data.local.results.length === 0
	) {
		return 'No local results found.'
	}

	const { results } = data.local
	const formattedResults = results
		.map((result: any, index: number) => {
			const { name, address, phone, rating, reviews_count, opening_hours } =
				result

			let details = `[${index + 1}] ${name}\n`
			details += address ? `Address: ${address}\n` : ''
			details += phone ? `Phone: ${phone}\n` : ''

			if (rating !== undefined) {
				details += `Rating: ${rating}/5`
				details +=
					reviews_count !== undefined ? ` (${reviews_count} reviews)\n` : '\n'
			}

			details += opening_hours ? `Hours: ${opening_hours}\n` : ''

			return details
		})
		.join('\n')

	return `Local search results for: "${originalQuery}"\n\n${formattedResults}`
}
