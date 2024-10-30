'use client'

import { useState } from 'react'
import { Button } from '../ui/button'
import { generateText } from 'ai'
import { createGoogleGenerativeAI } from '@ai-sdk/google'

const google = createGoogleGenerativeAI({
	apiKey: '',
})

export const GoogleChatInput = () => {
	const [message, setMessage] = useState('')
	const [responseList, setResponseList] = useState<string[]>([])

	const sendMessage = async () => {
		if (message.length == 0) {
			return
		}
		console.log('Sending message:', message)
		// Send message to Google AI Chat API
		const { text } = await generateText({
			model: google('gemini-1.5-flash-latest'),

			prompt: message,
			headers: {
				apiKey: 'AIzaSyC8sc3Y642NgxK8EmJCFBCFw5-0RbvWFFQ',
			},
		})
		setMessage('')
		setResponseList((prev) => [...prev, text])
	}

	return (
		<>
			<div>
				{responseList.map((response, index) => (
					<div key={index} className="flex flex-col gap-2">
						<div className="flex flex-row items-start gap-1">
							<div className="flex-shrink-0 w-6 h-6 bg-chart-1 rounded-md"></div>
							<div className="flex-grow text-sm md:text-lg text-gray-900">
								{response}
							</div>
						</div>
						<div className="flex-grow"></div>
					</div>
				))}
			</div>
			<div className="flex flex-row w-full items-center justify-between gap-3">
				<input
					type="text"
					value={message}
					onChange={(e) => setMessage(e.target.value)}
					placeholder="Type a message..."
					className="w-full p-3  text-md md:text-lg rounded-md focus:ring-2 focus:ring-yellow-600"
				/>
				<Button
					className="min-w-fit h-full p-3 w-[7rem] text-md md:text-lg text-white bg-yellow-600 rounded-md hover:bg-yellow-700"
					onClick={sendMessage}
				>
					Send
				</Button>
			</div>
		</>
	)
}
