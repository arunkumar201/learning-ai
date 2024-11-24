'use client'

import * as React from 'react'
import { Home, FileText, Settings, Menu, BotIcon } from 'lucide-react'

import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarTrigger,
	useSidebar,
} from '@/components/ui/sidebar'
import { CHAT_SIDEBAR } from '@/constants'
import Link from 'next/link'
import { cn } from '@/lib/utils'

export function ChatSidebar() {
	const { state } = useSidebar()
	return (
		<Sidebar collapsible="icon" className="w-[10rem] min-w-[4rem]">
			<div
				className={cn(
					'relative flex items-center p-2 flex-col justify-between',
					state === 'collapsed' && 'justify-start'
				)}
			>
				<BotIcon className="h-6 w-6" />
				{state === 'expanded' && (
					<span className="h-6 text-gray-500 dark:text-gray-100 hidden md:block">
						Apna Chat
					</span>
				)}
			</div>
			<SidebarHeader
				className={cn(
					'w-full h-16 flex items-start justify-start relative top-[-4rem] left-[9rem] z-[1000]',
					state === 'collapsed' && 'justify-end left-[3rem]'
				)}
			>
				<SidebarTrigger className="w-3 h-3 top-0"></SidebarTrigger>
			</SidebarHeader>
			<SidebarContent className="flex flex-col justify-start flex-grow p-2">
				<SidebarMenu>
					{CHAT_SIDEBAR.map((item) => {
						return (
							<SidebarMenuItem key={item.id}>
								<SidebarMenuButton
									asChild
									tooltip={item.tooltip}
									className={`hover:bg-gray-400 ${
										item.isActive ? 'bg-gray-300' : ''
									}`}
								>
									<Link href={item.href}>
										<item.icon className="h-5 w-5" />
										<span className="ml-3">{item.label}</span>
									</Link>
								</SidebarMenuButton>
							</SidebarMenuItem>
						)
					})}
				</SidebarMenu>
			</SidebarContent>
			<SidebarFooter className="h-16 flex items-center justify-center">
				<span className="text-xs text-muted-foreground">© 2024</span>
			</SidebarFooter>
		</Sidebar>
	)
}
