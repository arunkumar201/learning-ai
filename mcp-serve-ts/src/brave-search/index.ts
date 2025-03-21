const BRAVE_API_KEY = process.env.BRAVE_API_KEY!

if (!BRAVE_API_KEY) {
	console.error('BRAVE_API_KEY is not set')
	process.exit(1)
}

