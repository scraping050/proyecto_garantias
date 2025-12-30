'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { LayoutDashboard, Briefcase, TrendingUp, FileText, Settings, LogOut, Search, BarChart3, PieChart } from 'lucide-react'
import { useState, useEffect } from 'react'
import { LogoutModal } from '@/components/ui/logout-modal'

export function ExecutiveSidebar() {
    const pathname = usePathname()
    const router = useRouter()
    const [user, setUser] = useState<any>(null)
    const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false)

    // Get user from localStorage
    // Get user from localStorage
    useEffect(() => {
        const userData = localStorage.getItem('user')
        if (userData) {
            try {
                setUser(JSON.parse(userData))
            } catch (e) {
                console.error("Error parsing user data", e)
            }
        }
    }, [])

    const handleLogoutClick = () => {
        setIsLogoutModalOpen(true)
    }

    const handleConfirmLogout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('selectedProfile')
        router.push('/')
    }

    const menuItems = [
        {
            section: 'ANÁLISIS',
            items: [
                { name: 'Vista General', href: '/dashboard', icon: LayoutDashboard },
                { name: 'Ecommerce', href: '/dashboard/ecommerce', icon: BarChart3 },
                { name: 'Búsqueda', href: '/busqueda-licitaciones', icon: Search },
                { name: 'Proyectos', href: '/licitaciones', icon: Briefcase },
                { name: 'Tendencias', href: '/tendencias', icon: TrendingUp },
            ]
        },
        {
            section: 'REPORTES',
            items: [
                { name: 'Reportes', href: '/reportes', icon: PieChart },
            ]
        },
        {
            section: 'CONFIGURACIÓN',
            items: [
                { name: 'Preferencias', href: '/preferencias', icon: Settings },
            ]
        }
    ]

    return (
        <div className="w-64 bg-[#f8f9fa] dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col h-screen">
            {/* Logo */}
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">MQS</h1>
                <p className="text-sm text-gray-600 dark:text-gray-400 tracking-wide">ANALYTICS</p>
            </div>

            {/* Navigation */}
            <nav className="flex-1 overflow-y-auto py-6">
                {menuItems.map((section, idx) => (
                    <div key={idx} className="mb-6">
                        <h3 className="px-6 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
                            {section.section}
                        </h3>
                        <div className="space-y-1">
                            {section.items.map((item) => {
                                const Icon = item.icon
                                const isActive = pathname === item.href

                                return (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        className={`flex items-center gap-3 px-6 py-3 text-sm font-medium transition-colors ${isActive
                                            ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 border-r-4 border-blue-700 dark:border-blue-500'
                                            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                                            }`}
                                    >
                                        <Icon className="w-5 h-5" />
                                        {item.name}
                                    </Link>
                                )
                            })}
                        </div>
                    </div>
                ))}
            </nav>

            {/* User Section */}
            <div className="border-t border-gray-200 dark:border-gray-700 p-6">
                <div className="mb-4">
                    <h4 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
                        ANALISTA
                    </h4>
                    {user && (
                        <div className="flex items-center gap-3 mb-3">
                            <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
                                {user.nombre?.charAt(0) || 'M'}
                            </div>
                            <div>
                                <p className="text-sm font-medium text-gray-900 dark:text-white">{user.nombre}</p>
                                <p className="text-xs text-gray-500 dark:text-gray-400">{user.perfil}</p>
                            </div>
                        </div>
                    )}
                </div>
                <button
                    onClick={handleLogoutClick}
                    className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium transition-colors hover:text-red-600 dark:hover:text-red-400 group"
                >
                    <LogOut className="w-4 h-4 group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors" />
                    SALIR
                </button>
            </div>

            <LogoutModal
                open={isLogoutModalOpen}
                onOpenChange={setIsLogoutModalOpen}
                onConfirm={handleConfirmLogout}
            />
        </div>
    )
}
