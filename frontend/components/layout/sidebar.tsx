'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
    LayoutDashboard,
    FileText,
    Building2,
    Settings,
    ChevronLeft,
    ChevronRight,
    Search,
    BarChart3,
    PieChart
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { useState, useEffect } from 'react'

const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Ecommerce', href: '/dashboard/ecommerce', icon: BarChart3 },
    { name: 'Búsqueda', href: '/busqueda-licitaciones', icon: Search },
    { name: 'Reportes', href: '/reportes', icon: PieChart },
    { name: 'Licitaciones', href: '/licitaciones', icon: FileText },
    { name: 'Bancos', href: '/bancos', icon: Building2 },
    { name: 'Configuración', href: '/configuracion', icon: Settings },
]

export function Sidebar() {
    const pathname = usePathname()
    const [collapsed, setCollapsed] = useState(false)

    // Load collapsed state from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('sidebar-collapsed')
        if (saved !== null) {
            setCollapsed(JSON.parse(saved))
        }
    }, [])

    // Save collapsed state to localStorage
    const toggleCollapsed = () => {
        const newState = !collapsed
        setCollapsed(newState)
        localStorage.setItem('sidebar-collapsed', JSON.stringify(newState))
    }

    return (
        <div
            className={cn(
                "relative flex flex-col border-r bg-card transition-all duration-300",
                collapsed ? "w-16" : "w-64"
            )}
        >
            {/* Logo */}
            <div className="flex h-16 items-center border-b px-4">
                {!collapsed && (
                    <Link href="/dashboard" className="flex items-center gap-2">
                        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                            <FileText className="h-5 w-5" />
                        </div>
                        <span className="text-lg font-semibold">SEACE Monitor</span>
                    </Link>
                )}
                {collapsed && (
                    <Link href="/dashboard" className="flex items-center justify-center w-full">
                        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                            <FileText className="h-5 w-5" />
                        </div>
                    </Link>
                )}
            </div>

            {/* Navigation */}
            <nav className="flex-1 space-y-1 p-2">
                {navigation.map((item) => {
                    const isActive = pathname === item.href || pathname?.startsWith(item.href + '/')
                    return (
                        <Link
                            key={item.name}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                                isActive
                                    ? "bg-primary text-primary-foreground"
                                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                                collapsed && "justify-center"
                            )}
                            title={collapsed ? item.name : undefined}
                        >
                            <item.icon className="h-5 w-5 flex-shrink-0" />
                            {!collapsed && <span>{item.name}</span>}
                        </Link>
                    )
                })}
            </nav>

            {/* Collapse Toggle */}
            <div className="border-t p-2">
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={toggleCollapsed}
                    className={cn("w-full", collapsed && "px-2")}
                >
                    {collapsed ? (
                        <ChevronRight className="h-4 w-4" />
                    ) : (
                        <>
                            <ChevronLeft className="h-4 w-4 mr-2" />
                            <span>Colapsar</span>
                        </>
                    )}
                </Button>
            </div>
        </div>
    )
}
