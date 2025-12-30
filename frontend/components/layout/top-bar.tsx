'use client'

import { usePathname } from 'next/navigation'
import { ChevronRight } from 'lucide-react'

export function TopBar() {
    const pathname = usePathname()

    // Generate breadcrumbs from pathname
    const breadcrumbs = pathname
        ?.split('/')
        .filter(Boolean)
        .map((segment, index, array) => {
            const href = '/' + array.slice(0, index + 1).join('/')
            const label = segment.charAt(0).toUpperCase() + segment.slice(1)
            return { label, href }
        }) || []

    return (
        <div className="flex h-16 items-center justify-between border-b bg-card px-6">
            {/* Breadcrumbs */}
            <div className="flex items-center gap-2 text-sm">
                <span className="text-muted-foreground">Inicio</span>
                {breadcrumbs.map((crumb, index) => (
                    <div key={crumb.href} className="flex items-center gap-2">
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                        <span
                            className={
                                index === breadcrumbs.length - 1
                                    ? "font-medium text-foreground"
                                    : "text-muted-foreground"
                            }
                        >
                            {crumb.label}
                        </span>
                    </div>
                ))}
            </div>

            {/* Placeholder for theme toggle */}
            <div className="flex items-center gap-4">
                {/* Theme toggle removed temporarily */}
            </div>
        </div>
    )
}
