import dotenv from 'dotenv'
dotenv.config()

export const WEB_SEARCH_TOOL_DESCRIPTION = `

This tool performs a web search using the Brave Search API, making it ideal for retrieving general information, news, articles, and online content. It’s perfect for:

Broad information gathering on a wide range of topics.

Staying updated on recent events or trending topics.

Accessing diverse web sources for comprehensive insights.

Key Features:

Pagination: Supports offsets to navigate through multiple pages of results.

Content Filtering: Allows refining results based on specific criteria.

Freshness Controls: Ensures up-to-date and relevant information.

Usage Notes:

Maximum of 20 results per request.

Use the offset parameter for pagination to retrieve additional results.

This tool is designed to provide accurate, diverse, and timely information from the web, making it a powerful resource for research, fact-checking, and exploration.
`
export const LOCAL_SEARCH_TOOL_DESCRIPTION = `
This tool searches for local businesses, places, and services using Brave's Local Search API. It’s ideal for queries related to physical locations, such as:

Restaurants, cafes, and bars.

Retail stores, service providers, and businesses.

"Near me" searches or location-specific requests.

Returns Detailed Information:

Business Names and Addresses: Precise locations and contact details.

Ratings and Review Counts: Insights into user feedback and popularity.

Phone Numbers and Opening Hours: Practical details for planning visits.

Key Features:

Automatically falls back to web search if no local results are found.

Perfect for queries that imply proximity or mention specific locations.

Use this tool to find accurate, up-to-date information about nearby businesses and services, making it a valuable resource for location-based inquiries.`
