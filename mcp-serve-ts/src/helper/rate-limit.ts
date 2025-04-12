import { z } from 'zod'

export const rateLimitConfigSchema = z.object({
	perSecond: z.number().min(1).max(100).default(4),
	windowMs: z.number().min(1000).max(60000).default(1000),
})

export const rateLimitConfig = rateLimitConfigSchema.parse({
	perSecond: 4,
	windowMs: 1000,
})

interface RateLimitState {
	ip: string
	lastReset: number
	remaining: number
	blockedUntil?: number
}

const rateLimiter = new Map<string, RateLimitState>()

export class RateLimitError extends Error {
	constructor(message: string, public readonly retryAfter: number) {
		super(message)
		this.name = 'RateLimitError'
	}
}

export async function rateLimit(ip: string): Promise<void> {
	const now = Date.now()
	const state = rateLimiter.get(ip)

	if (state?.blockedUntil && now < state.blockedUntil) {
		throw new RateLimitError(
			'Rate limit exceeded. Please try again later.',
			Math.ceil((state.blockedUntil - now) / 1000)
		)
	}

	if (state) {
		if (now - state.lastReset >= rateLimitConfig.windowMs) {
			state.remaining = rateLimitConfig.perSecond
			state.lastReset = now
		}

		if (state.remaining <= 0) {
			const blockedUntil = now + rateLimitConfig.windowMs
			state.blockedUntil = blockedUntil
			rateLimiter.set(ip, state)
			throw new RateLimitError(
				'Rate limit exceeded. Please try again later.',
				Math.ceil(rateLimitConfig.windowMs / 1000)
			)
		}

		state.remaining--
		rateLimiter.set(ip, state)
	} else {
		rateLimiter.set(ip, {
			ip,
			lastReset: now,
			remaining: rateLimitConfig.perSecond - 1,
		})
	}
}
