export const rate_limit_config = {
	perSecond: 4,
}

//TODO: We will Replace with a more robust rate limiting mechanism
interface IRequest {
	ip: string
	last_reset: number
	remaining: number
}
const rateLimiter = new Map<string, IRequest>()

export const rateLimit = async (ip: string) => {
	if (rateLimiter.has(ip)) {
		const request = rateLimiter.get(ip)!
		const now = Date.now()

		// Check if we should reset the counter (1 second has passed)
		if (now - request.last_reset >= 1000) {
			request.remaining = rate_limit_config.perSecond
			request.last_reset = now
		}

		// Check if we've exceeded the rate limit
		if (request.remaining <= 0) {
			return false
		}

		// Decrement remaining requests and update
		request.remaining--
		rateLimiter.set(ip, request)
		return true
	} else {
		rateLimiter.set(ip, {
			ip,
			last_reset: Date.now(),
			remaining: rate_limit_config.perSecond - 1,
		})
		return true
	}
}
