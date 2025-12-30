import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

/**
 * Get bank-specific color classes
 */
export function getBankColor(bank: string | null): string {
    if (!bank) return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"

    const bankUpper = bank.toUpperCase()

    if (bankUpper.includes('SCOTIA')) {
        return "bg-scotiabank text-scotiabank-foreground"
    }
    if (bankUpper.includes('BCP')) {
        return "bg-bcp text-bcp-foreground"
    }
    if (bankUpper.includes('BBVA')) {
        return "bg-bbva text-bbva-foreground"
    }
    if (bankUpper.includes('INTERBANK')) {
        return "bg-interbank text-interbank-foreground"
    }
    if (bankUpper.includes('FOGAPI') || bankUpper.includes('SECREX')) {
        return "bg-fogapi text-fogapi-foreground"
    }

    return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
}

/**
 * Get status-specific color classes
 */
export function getStatusColor(status: string | null): string {
    if (!status) return "bg-gray-100 text-gray-800"

    const statusLower = status.toLowerCase()

    if (statusLower.includes('adjudicado')) {
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
    }
    if (statusLower.includes('desierto')) {
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
    }
    if (statusLower.includes('convocado')) {
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
    }
    if (statusLower.includes('cancelado')) {
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
    }

    return "bg-gray-100 text-gray-800"
}

/**
 * Copy text to clipboard with toast notification
 */
export async function copyToClipboard(text: string): Promise<boolean> {
    try {
        await navigator.clipboard.writeText(text)
        return true
    } catch (err) {
        console.error('Failed to copy:', err)
        return false
    }
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
    func: T,
    wait: number
): (...args: Parameters<T>) => void {
    let timeout: NodeJS.Timeout | null = null

    return function executedFunction(...args: Parameters<T>) {
        const later = () => {
            timeout = null
            func(...args)
        }

        if (timeout) clearTimeout(timeout)
        timeout = setTimeout(later, wait)
    }
}
