'use client'

import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'

const API_BASE_URL = '/api/tendencias'

// Filter state type
export interface TendenciasFilters {
    objeto_contratacion?: string
    tipo_procedimiento?: string
    estado_proceso?: string
    departamento?: string
    banco_garantia?: string
}

// Response types
export interface KPIsData {
    total_adjudicado: number
    cantidad_procesos: number
    ahorro_total: number
    total_estimado: number
    porcentaje_ahorro: number
}

export interface GeographicData {
    level: 'departamento' | 'provincia'
    parent: string | null
    data: Array<{
        location: string
        monto_total: number
        cantidad_procesos: number
        parent?: string
    }>
}

export interface BankRankingData {
    data: Array<{
        banco: string
        monto_total: number
        cantidad_garantias: number
    }>
}

export interface TemporalTrendData {
    year: number
    data: Array<{
        month: string
        month_num: number
        year: number
        monto_total: number
        cantidad: number
    }>
}

export interface TopProvidersData {
    data: Array<{
        proveedor: string
        ruc: string
        monto_total: number
        cantidad_contratos: number
    }>
    total: number
    limit: number
    offset: number
}

export interface SavingsGaugeData {
    monto_referencial: number
    monto_adjudicado: number
    ahorro: number
    porcentaje_ahorro: number
    porcentaje_ejecutado: number
    cantidad_procesos: number
    status: 'good' | 'moderate' | 'over_budget'
}

export interface ConsortiumMember {
    nombre_miembro: string
    ruc_miembro: string
    porcentaje_participacion: number
}

export interface ConsortiumData {
    data: Array<{
        nomenclatura: string
        descripcion: string
        proveedor_ganador: string
        ruc_ganador: string
        monto_adjudicado: number
        miembros: ConsortiumMember[]
        cantidad_miembros: number
    }>
    total: number
}

export interface FilterOptions {
    objetos_contratacion: string[]
    tipos_procedimiento: string[]
    estados_proceso: string[]
    departamentos: string[]
    bancos_garantia: string[]
}

// Custom hook for tendencias data
export function useTendencias() {
    const [filters, setFilters] = useState<TendenciasFilters>({})
    const [selectedDepartamento, setSelectedDepartamento] = useState<string | null>(null)
    const [consortiumSearch, setConsortiumSearch] = useState<string>('')

    // Build query params
    const buildQueryParams = (additionalParams: Record<string, any> = {}) => {
        const params = new URLSearchParams()
        Object.entries({ ...filters, ...additionalParams }).forEach(([key, value]) => {
            if (value !== undefined && value !== null && value !== '') {
                params.append(key, String(value))
            }
        })
        return params.toString()
    }

    // Fetch KPIs
    const kpis = useQuery<KPIsData>({
        queryKey: ['tendencias-kpis', filters],
        queryFn: async () => {
            const params = buildQueryParams()
            const response = await fetch(`${API_BASE_URL}/kpis?${params}`)
            if (!response.ok) throw new Error('Failed to fetch KPIs')
            return response.json()
        }
    })

    // Fetch Geographic Heat Map
    const geographicHeatmap = useQuery<GeographicData>({
        queryKey: ['tendencias-geographic', filters.objeto_contratacion, selectedDepartamento],
        queryFn: async () => {
            const params = buildQueryParams({
                departamento: selectedDepartamento
            })
            const response = await fetch(`${API_BASE_URL}/geographic-heatmap?${params}`)
            if (!response.ok) throw new Error('Failed to fetch geographic data')
            return response.json()
        }
    })

    // Fetch Bank Ranking
    const bankRanking = useQuery<BankRankingData>({
        queryKey: ['tendencias-bank-ranking', filters.tipo_procedimiento],
        queryFn: async () => {
            const params = buildQueryParams()
            const response = await fetch(`${API_BASE_URL}/bank-ranking?${params}`)
            if (!response.ok) throw new Error('Failed to fetch bank ranking')
            return response.json()
        }
    })

    // Fetch Temporal Trend
    const temporalTrend = useQuery<TemporalTrendData>({
        queryKey: ['tendencias-temporal-trend', filters.estado_proceso],
        queryFn: async () => {
            const params = buildQueryParams()
            const response = await fetch(`${API_BASE_URL}/temporal-trend?${params}`)
            if (!response.ok) throw new Error('Failed to fetch temporal trend')
            return response.json()
        }
    })

    // Fetch Top Providers
    const topProviders = useQuery<TopProvidersData>({
        queryKey: ['tendencias-top-providers', filters.banco_garantia],
        queryFn: async () => {
            const params = buildQueryParams()
            const response = await fetch(`${API_BASE_URL}/top-providers?${params}`)
            if (!response.ok) throw new Error('Failed to fetch top providers')
            return response.json()
        }
    })

    // Fetch Savings Gauge
    const savingsGauge = useQuery<SavingsGaugeData>({
        queryKey: ['tendencias-savings-gauge', filters.departamento],
        queryFn: async () => {
            const params = buildQueryParams()
            const response = await fetch(`${API_BASE_URL}/savings-gauge?${params}`)
            if (!response.ok) throw new Error('Failed to fetch savings gauge')
            return response.json()
        }
    })

    // Fetch Consortium Breakdown
    const consortiumBreakdown = useQuery<ConsortiumData>({
        queryKey: ['tendencias-consortium', consortiumSearch],
        queryFn: async () => {
            const params = new URLSearchParams()
            if (consortiumSearch) {
                params.append('search', consortiumSearch)
            }
            const response = await fetch(`${API_BASE_URL}/consortium-breakdown?${params}`)
            if (!response.ok) throw new Error('Failed to fetch consortium data')
            return response.json()
        },
        enabled: consortiumSearch.length >= 3 || consortiumSearch === ''
    })

    // Fetch Filter Options
    const filterOptions = useQuery<FilterOptions>({
        queryKey: ['tendencias-filter-options'],
        queryFn: async () => {
            const response = await fetch(`${API_BASE_URL}/filter-options`)
            if (!response.ok) throw new Error('Failed to fetch filter options')
            return response.json()
        }
    })

    // Update filters
    const updateFilters = (newFilters: Partial<TendenciasFilters>) => {
        setFilters(prev => ({ ...prev, ...newFilters }))
    }

    // Reset filters
    const resetFilters = () => {
        setFilters({})
        setSelectedDepartamento(null)
        setConsortiumSearch('')
    }

    return {
        // Data
        kpis,
        geographicHeatmap,
        bankRanking,
        temporalTrend,
        topProviders,
        savingsGauge,
        consortiumBreakdown,
        filterOptions,

        // State
        filters,
        selectedDepartamento,
        consortiumSearch,

        // Actions
        updateFilters,
        resetFilters,
        setSelectedDepartamento,
        setConsortiumSearch
    }
}
