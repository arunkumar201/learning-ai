export interface WebSearchResponse {
	web?: {
		results?: WebSearchResult[]
		count?: number
		more_results_available?: boolean
	}
	query?: {
		original?: string
		show_strict_warning?: boolean
		spellcheck_off?: boolean
	}
}

export interface WebSearchResult {
	title: string
	url: string
	description?: string
	age?: string
	family_friendly?: boolean
}

export interface LocalSearchResponse {
	local?: {
		results?: LocalSearchResult[]
		more_results_available?: boolean
	}
	query?: {
		original?: string
	}
}

export interface LocalSearchResult {
	name: string
	address?: string
	phone?: string
	rating?: number
	reviews_count?: number
	opening_hours?: string
	website?: string
	categories?: string[]
	location?: {
		lat: number
		lng: number
	}
}

/**
 * API request types
 */

export interface WebSearchParams {
	query: string
	count?: number
	offset?: number
}

export interface LocalSearchParams {
	query: string
	count?: number
}
