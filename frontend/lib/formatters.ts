/**
 * Format currency in PEN (Peruvian Soles)
 */
export function formatCurrency(amount: number | null | undefined): string {
    if (amount === null || amount === undefined) return 'N/A'

    return new Intl.NumberFormat('es-PE', {
        style: 'currency',
        currency: 'PEN',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(amount)
}

/**
 * Format currency in compact form (e.g., S/ 1.2M)
 */
export function formatCurrencyCompact(amount: number | null | undefined): string {
    if (amount === null || amount === undefined) return 'N/A'

    return new Intl.NumberFormat('es-PE', {
        style: 'currency',
        currency: 'PEN',
        notation: 'compact',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
    }).format(amount)
}

/**
 * Format date in DD/MM/YYYY format
 */
export function formatDate(date: string | null | undefined): string {
    if (!date) return 'N/A'

    try {
        const d = new Date(date)
        return new Intl.DateTimeFormat('es-PE', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
        }).format(d)
    } catch {
        return 'N/A'
    }
}

/**
 * Format date in relative time (e.g., "hace 2 días")
 */
export function formatDateRelative(date: string | null | undefined): string {
    if (!date) return 'N/A'

    try {
        const d = new Date(date)
        const now = new Date()
        const diffMs = now.getTime() - d.getTime()
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

        if (diffDays === 0) return 'Hoy'
        if (diffDays === 1) return 'Ayer'
        if (diffDays < 7) return `Hace ${diffDays} días`
        if (diffDays < 30) return `Hace ${Math.floor(diffDays / 7)} semanas`
        if (diffDays < 365) return `Hace ${Math.floor(diffDays / 30)} meses`
        return `Hace ${Math.floor(diffDays / 365)} años`
    } catch {
        return 'N/A'
    }
}

/**
 * Format percentage
 */
export function formatPercent(value: number | null | undefined): string {
    if (value === null || value === undefined) return 'N/A'

    return new Intl.NumberFormat('es-PE', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
    }).format(value / 100)
}

/**
 * Format RUC with dashes (20-12345678-9)
 */
export function formatRUC(ruc: string | null | undefined): string {
    if (!ruc) return 'N/A'

    // Remove any existing dashes
    const clean = ruc.replace(/-/g, '')

    // Format as XX-XXXXXXXX-X if 11 digits
    if (clean.length === 11) {
        return `${clean.slice(0, 2)}-${clean.slice(2, 10)}-${clean.slice(10)}`
    }

    return ruc
}

/**
 * Format large numbers with K, M, B suffixes
 */
export function formatNumber(num: number | null | undefined): string {
    if (num === null || num === undefined) return 'N/A'

    if (num >= 1_000_000_000) {
        return `${(num / 1_000_000_000).toFixed(1)}B`
    }
    if (num >= 1_000_000) {
        return `${(num / 1_000_000).toFixed(1)}M`
    }
    if (num >= 1_000) {
        return `${(num / 1_000).toFixed(1)}K`
    }

    return num.toString()
}

/**
 * Format currency with custom "mil millones" notation instead of MRD
 */
export function formatCurrencyCustom(amount: number | null | undefined): string {
    if (amount === null || amount === undefined) return 'N/A'

    if (amount >= 1_000_000_000) {
        return `S/ ${(amount / 1_000_000_000).toFixed(1)} mil millones`
    }
    if (amount >= 1_000_000) {
        return `S/ ${(amount / 1_000_000).toFixed(1)}M`
    }
    if (amount >= 1_000) {
        return `S/ ${(amount / 1_000).toFixed(0)}K`
    }

    return new Intl.NumberFormat('es-PE', {
        style: 'currency',
        currency: 'PEN',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(amount)
}
