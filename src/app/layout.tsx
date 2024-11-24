import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { SidebarProvider } from '@/components/ui/sidebar'
import { ChatSidebar } from '@/components/sidebar'

const geistSans = localFont({
	src: './fonts/GeistVF.woff',
	variable: '--font-geist-sans',
	weight: '100 900',
})
const geistMono = localFont({
	src: './fonts/GeistMonoVF.woff',
	variable: '--font-geist-mono',
	weight: '100 900',
})

export const metadata: Metadata = {
	title: 'AI Dev with next AI SDK',
	description: 'AI Development with next AI SDK',
}

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode
}>) {
	return (
		<html lang="en">
			<body
				className={`${geistSans.variable} ${geistMono.variable} antialiased`}
			>
				<SidebarProvider>
					<div className="flex h-screen w-full">
						<ChatSidebar />
						<main className="flex-1 p-6 bg-background w-full">{children}</main>
					</div>
				</SidebarProvider>
			</body>
		</html>
	)
}
