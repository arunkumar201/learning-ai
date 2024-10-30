import { GoogleChat } from '@/components/google-chat/google-chat'
import { Suspense } from 'react'
export default function Home() {
	return (
		<div className="bg-gray-700 text-gray-50 grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-10 sm:p-20 font-[family-name:var(--font-geist-sans)]">
			<h1 className="text-xl md:text-3xl underline leading-7 italic">
				AI Development with next AI SDK{' '}
			</h1>
			<GoogleChat />
		</div>
	)
}
