'use client'

import { useQuery } from '@tanstack/react-query'
import { fetchDashboardKPIs, fetchLicitaciones, fetchLicitacionDetail } from '@/lib/api'
import type { LicitacionesFilters } from '@/types'

/**
 * Hook to fetch dashboard KPIs
 */
export function useDashboardKPIs() {
    return useQuery({
        queryKey: ['dashboard', 'kpis'],
        queryFn: fetchDashboardKPIs,
        staleTime: 5 * 60 * 1000, // 5 minutes
        refetchOnWindowFocus: false,
    })
}

/**
 * Hook to fetch paginated licitaciones with filters
 */
export function useLicitaciones(filters: LicitacionesFilters = {}) {
    return useQuery({
        queryKey: ['licitaciones', filters],
        queryFn: () => fetchLicitaciones(filters),
        staleTime: 2 * 60 * 1000, // 2 minutes
        keepPreviousData: true, // Keep previous data while fetching new page
    })
}

/**
 * Hook to fetch single licitacion detail
 */
export function useLicitacionDetail(id: number) {
    return useQuery({
        queryKey: ['licitacion', id],
        queryFn: () => fetchLicitacionDetail(id),
        staleTime: 5 * 60 * 1000, // 5 minutes
        enabled: !!id, // Only fetch if id is provided
    })
}
