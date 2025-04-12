
type Interval = 'second' | 'minute' | 'hour' | 'day'

interface RateLimiterOptions {
	tokensPerInterval: number
	interval: Interval
	maxTokens?: number
}

interface RateLimiter {
	consume: (tokens?: number) => Promise<void>
	getTokens: () => number
	resetTokens: () => void
}


export function createRateLimiter(options: RateLimiterOptions): RateLimiter {
	const { tokensPerInterval, interval, maxTokens = tokensPerInterval } = options

	const intervalMs = getIntervalMs(interval)

	let tokens = maxTokens
	let lastRefill = Date.now()

	function refillTokens() {
		const now = Date.now()
		const timePassed = now - lastRefill

		if (timePassed > 0) {
			const tokensToAdd = Math.floor(
				(timePassed / intervalMs) * tokensPerInterval
			)

			if (tokensToAdd > 0) {
				tokens = Math.min(tokens + tokensToAdd, maxTokens)
				lastRefill = now
			}
		}
	}

	async function consume(count = 1): Promise<void> {
		refillTokens()

		if (tokens >= count) {
			tokens -= count
			return Promise.resolve()
		}

		const tokensNeeded = count - tokens
		const waitTime = Math.ceil((tokensNeeded / tokensPerInterval) * intervalMs)

		return new Promise((resolve) => {
			setTimeout(() => {
				tokens = maxTokens - count
				lastRefill = Date.now()
				resolve()
			}, waitTime)
		})
	}

	return {
		consume,
		getTokens: () => tokens,
		resetTokens: () => {
			tokens = maxTokens
			lastRefill = Date.now()
		},
	}
}

function getIntervalMs(interval: Interval): number {
	switch (interval) {
		case 'second':
			return 1000
		case 'minute':
			return 60 * 1000
		case 'hour':
			return 60 * 60 * 1000
		case 'day':
			return 24 * 60 * 60 * 1000
	}
}
