import { env } from '@/env'

export const sseConfig = {
	path: env.SSE_ENDPOINT,
	corsOrigins: '*',
}

export const braveConfig = {
	apiKey: env.BRAVE_API_KEY,
	baseUrl: 'https://api.search.brave.com/res/v1',
}

export const appConfig = {
	port: env.PORT,
	environment: env.NODE_ENV,
	isDevelopment: env.NODE_ENV === 'development',
	isProduction: env.NODE_ENV === 'production',
	isTest: env.NODE_ENV === 'test',
}
