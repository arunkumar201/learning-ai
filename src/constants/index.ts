import { Home, MessageCircleIcon } from 'lucide-react'

export interface IChatSidebarItem {
	id: string
	label: string
	href: string
	tooltip?: string
	isActive?: boolean
	icon?: React.FC<React.SVGProps<SVGSVGElement>>
}
export const CHAT_SIDEBAR = [
	{
		href: '/dashboard',
		label: 'Dashboard',
		id: 'dashboard',
		icon: Home,
		isActive: false,
		tooltip: 'Go to Dashboard',
	},
	{
		href: '/messages',
		label: 'Messages',
		id: 'messages',
		icon: MessageCircleIcon,
		isActive: false,
		tooltip: 'Go to Messages',
	},
] satisfies IChatSidebarItem[]
