import dotenv from 'dotenv'
import { z } from 'zod'

dotenv.config()

export const envSchema = z.object({
	PORT: z.string().default('3001').transform(Number),
	NODE_ENV: z
		.enum(['development', 'production', 'test'])
		.default('development'),
	SSE_ENDPOINT: z.string().default('/sse'),
	BRAVE_API_KEY: z.string().min(1, 'BRAVE_API_KEY is required'),
})

export function validateEnv() {
	try {
		return envSchema.parse(process.env)
	} catch (error) {
		if (error instanceof z.ZodError) {
			console.error('Environment validation error:', error.errors)
		} else {
			console.error('Unexpected error during environment validation:', error)
		}

		if (process.env.NODE_ENV === 'production') {
			process.exit(1)
		}

		return envSchema.parse({})
	}
}

export const env = validateEnv()
