import { Suspense } from 'react'
import { GoogleChatInput } from './google-chat-input'

export const GoogleChat = () => {
	return (
		<div
			className="flex flex-col justify-between
		 text-gray-900 rounded-2xl shadow-2xl border-2 bg-gray-200 border-yellow-600 min-h-[20rem] h-full  max-w-[45rem] w-full px-10"
		>
			<div className="flex flex-col gap-4 justify-start items-center">
				<h1 className="text-md md:text-xl text-center p-2">
					Welcome to Google AI Chat
				</h1>
			</div>
			<div className="w-full flex flex-col gap-2 mb-3 justify-start items-end ">
				<Suspense fallback={<div>Loading...</div>}>
					<GoogleChatInput />
				</Suspense>
			</div>
		</div>
	)
}
