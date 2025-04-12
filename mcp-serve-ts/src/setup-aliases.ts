import module from 'module'
import { dirname, resolve } from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Get the custom require function that allows aliasing
const originalRequire = module.createRequire(import.meta.url)

// Configure the path aliases
const aliases: Record<string, string> = {
	'@': resolve(__dirname, '.'),
	'@api': resolve(__dirname, 'api'),
	'@config': resolve(__dirname, 'config'),
	'@core': resolve(__dirname, 'core'),
	'@env': resolve(__dirname, 'env.ts'),
	'@types': resolve(__dirname, 'types'),
	'@tools': resolve(__dirname, 'tools'),
	'@utils': resolve(__dirname, 'utils'),
	'@middleware': resolve(__dirname, 'middleware'),
}

// Register the aliases with Node.js module resolution
Object.entries(aliases).forEach(([alias, path]) => {
	// This doesn't actually modify the Node.js module resolution,
	// but it's here as a reference for what we're mapping
	console.debug(`Path alias: ${alias} -> ${path}`)
})

// Bun handles path aliases according to tsconfig.json when using ESM imports
