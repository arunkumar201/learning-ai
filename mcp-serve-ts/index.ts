import { sseConfig } from '@/config'
import { createMcpServer } from '@/core/mcp/server'
import { createSSEServer } from '@/core/mcp/sse-server'
import { env } from '@/env'

const mcpServer = createMcpServer()

const sseServer = createSSEServer(mcpServer, sseConfig)
const PORT = env.PORT
const inspectorPort = 6274

sseServer.listen(PORT, () => {
	console.log('MCP Server started successfully')
	console.log('--------------------------------')
	console.log(`🔌 Port:           ${PORT}`)
	console.log(`🌍 Mode:           ${env.NODE_ENV}`)
	console.log(`📡 SSE Path:       ${sseConfig.path}`)
	console.log(`🧪 Inspector URL:  http://localhost:${inspectorPort}`)
	console.log('--------------------------------')
})
