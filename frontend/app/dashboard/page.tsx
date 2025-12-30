'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ExecutiveSidebar } from '@/components/layout/executive-sidebar'
import { TrendingUp, TrendingDown, DollarSign, FileText, CheckCircle, XCircle, Play } from 'lucide-react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Button } from '@/components/ui/button'

interface KPIData {
    monto_total_adjudicado: number
    total_licitaciones: number
    top_bancos: Array<{ nombre: string, total: number }>
    top_entidades: Array<{ nombre: string, total: number }>
}

export default function DashboardPage() {
    const router = useRouter()
    const [kpis, setKpis] = useState<KPIData | null>(null)
    const [monthlyTrend, setMonthlyTrend] = useState<any[]>([])
    const [distribution, setDistribution] = useState<any[]>([])
    const [statusStats, setStatusStats] = useState<any[]>([])
    const [filterOptions, setFilterOptions] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [scrapingLoading, setScrapingLoading] = useState(false)
    const [userName, setUserName] = useState('')

    // Filters
    const [filters, setFilters] = useState({
        estado: '',
        aseguradora: '',
        tipo_entidad: '',
        objeto: ''
    })

    useEffect(() => {
        // Check authentication
        const token = localStorage.getItem('token')
        const userStr = localStorage.getItem('user')
        if (!token) {
            router.push('/login')
            return
        }

        if (userStr) {
            try {
                const userData = JSON.parse(userStr)
                setUserName(userData.nombre || 'Usuario')
            } catch (e) {
                console.error('Error parsing user data', e)
            }
        }

        // Load filter options
        loadFilterOptions()

        // Load initial data
        loadDashboardData()
    }, [router])

    const loadFilterOptions = async () => {
        try {
            const response = await fetch('/api/dashboard/filter-options')
            const data = await response.json()
            setFilterOptions(data)
        } catch (error) {
            console.error('Error loading filter options:', error)
        }
    }

    const loadDashboardData = async () => {
        setLoading(true)
        try {
            // Build query string
            const params = new URLSearchParams()
            if (filters.estado) params.append('estado', filters.estado)
            if (filters.aseguradora) params.append('aseguradora', filters.aseguradora)
            if (filters.tipo_entidad) params.append('tipo_entidad', filters.tipo_entidad)
            if (filters.objeto) params.append('objeto', filters.objeto)

            const queryString = params.toString()
            const baseUrl = '/api/dashboard'

            // Load KPIs
            const kpisResponse = await fetch(`${baseUrl}/kpis${queryString ? '?' + queryString : ''}`)
            const kpisData = await kpisResponse.json()
            setKpis(kpisData)

            // Load monthly trend
            const trendResponse = await fetch(`${baseUrl}/monthly-trend`)
            const trendData = await trendResponse.json()
            setMonthlyTrend(trendData.data || [])

            // Load distribution
            const distResponse = await fetch(`${baseUrl}/distribution-by-type`)
            const distData = await distResponse.json()
            setDistribution(distData.data || [])

            // Load status stats
            const statsResponse = await fetch(`${baseUrl}/stats-by-status`)
            const statsData = await statsResponse.json()
            setStatusStats(statsData.data || [])

        } catch (error) {
            console.error('Error loading dashboard data:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleFilterChange = (filterName: string, value: string) => {
        setFilters(prev => ({
            ...prev,
            [filterName]: value
        }))
    }

    const handleApplyFilters = () => {
        loadDashboardData()
    }

    const handleRunScraping = async () => {
        setScrapingLoading(true)
        try {
            const response = await fetch('/api/scraping/run', {
                method: 'POST'
            })
            const data = await response.json()
            alert(data.message)
            // Reload data after scraping
            setTimeout(() => {
                loadDashboardData()
            }, 2000)
        } catch (error) {
            console.error('Error running scraping:', error)
            alert('Error al ejecutar el scraping')
        } finally {
            setScrapingLoading(false)
        }
    }

    // Calculate stats
    const totalApproved = statusStats.find(s => s.status === 'Adjudicado')?.count || 0
    const totalRejected = statusStats.find(s => s.status === 'Desierto')?.count || 0
    const approvalRate = kpis ? ((totalApproved / kpis.total_licitaciones) * 100).toFixed(1) : '0'
    const avgAmount = kpis && kpis.total_licitaciones > 0
        ? (kpis.monto_total_adjudicado / kpis.total_licitaciones).toFixed(0)
        : '0'

    const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

    if (loading) {
        return (
            <div className="flex h-screen">
                <ExecutiveSidebar />
                <div className="flex-1 flex items-center justify-center">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                        <p className="text-gray-600">Cargando dashboard...</p>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
            <ExecutiveSidebar />

            <div className="flex-1 overflow-y-auto">
                {/* Header */}
                <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">DASHBOARD EJECUTIVO</h1>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Panel de control y análisis de garantías</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <span className="text-sm text-gray-600 dark:text-gray-400">Usuario: <span className="font-medium text-gray-900 dark:text-white">{userName}</span></span>
                            <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
                                M
                            </div>
                        </div>
                    </div>
                </div>

                {/* Filters */}
                <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-8 py-4">
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                        <div>
                            <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 uppercase tracking-wide">Estado</label>
                            <select
                                value={filters.estado}
                                onChange={(e) => handleFilterChange('estado', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todos</option>
                                {filterOptions?.estados?.map((e: string) => (
                                    <option key={e} value={e}>{e}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 uppercase tracking-wide">Aseguradora</label>
                            <select
                                value={filters.aseguradora}
                                onChange={(e) => handleFilterChange('aseguradora', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todas</option>
                                {filterOptions?.aseguradoras?.map((a: string) => (
                                    <option key={a} value={a}>{a}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 uppercase tracking-wide">Tipo Entidad</label>
                            <select
                                value={filters.tipo_entidad}
                                onChange={(e) => handleFilterChange('tipo_entidad', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todos</option>
                                {filterOptions?.tipos_entidad?.map((t: string) => (
                                    <option key={t} value={t}>{t}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 uppercase tracking-wide">Objeto</label>
                            <select
                                value={filters.objeto}
                                onChange={(e) => handleFilterChange('objeto', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todos</option>
                                {filterOptions?.objetos?.map((o: string) => (
                                    <option key={o} value={o}>{o}</option>
                                ))}
                            </select>
                        </div>

                        <div className="flex items-end gap-2">
                            <Button onClick={handleApplyFilters} className="flex-1 bg-blue-600 hover:bg-blue-700">
                                Aplicar
                            </Button>
                            <Button
                                onClick={handleRunScraping}
                                disabled={scrapingLoading}
                                className="bg-green-600 hover:bg-green-700"
                            >
                                <Play className="w-4 h-4 mr-2" />
                                {scrapingLoading ? 'Ejecutando...' : 'ETL'}
                            </Button>
                        </div>
                    </div>
                </div>

                {/* KPI Cards */}
                <div className="px-8 py-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        {/* Monto Total */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-green-100 rounded-lg">
                                    <DollarSign className="w-6 h-6 text-green-600" />
                                </div>
                                <div className="flex items-center gap-1 text-sm font-medium text-green-600">
                                    <TrendingUp className="w-4 h-4" />
                                    +12.5%
                                </div>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 font-medium mb-1">MONTO TOTAL</p>
                                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                                    S/ {kpis ? (kpis.monto_total_adjudicado / 1000000).toFixed(1) : '0'}M
                                </p>
                                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">Cartera activa 2024</p>
                            </div>
                        </div>

                        {/* Total Proyectos */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-cyan-100 rounded-lg">
                                    <FileText className="w-6 h-6 text-cyan-600" />
                                </div>
                                <div className="flex items-center gap-1 text-sm font-medium text-cyan-600">
                                    <TrendingUp className="w-4 h-4" />
                                    +8.3%
                                </div>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 font-medium mb-1">TOTAL PROYECTOS</p>
                                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                                    {kpis?.total_licitaciones.toLocaleString() || '0'}
                                </p>
                                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">En gestión activa</p>
                            </div>
                        </div>

                        {/* Aprobados */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-yellow-100 rounded-lg">
                                    <CheckCircle className="w-6 h-6 text-yellow-600" />
                                </div>
                                <div className="flex items-center gap-1 text-sm font-medium text-yellow-600">
                                    <TrendingUp className="w-4 h-4" />
                                    +15.2%
                                </div>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 font-medium mb-1">APROBADOS</p>
                                <p className="text-3xl font-bold text-gray-900 dark:text-white">{totalApproved}</p>
                                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">Tasa de aprobación {approvalRate}%</p>
                            </div>
                        </div>

                        {/* Rechazados */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-red-100 rounded-lg">
                                    <XCircle className="w-6 h-6 text-red-600" />
                                </div>
                                <div className="flex items-center gap-1 text-sm font-medium text-red-600">
                                    <TrendingDown className="w-4 h-4" />
                                    -3.1%
                                </div>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 font-medium mb-1">RECHAZADOS</p>
                                <p className="text-3xl font-bold text-gray-900 dark:text-white">{totalRejected}</p>
                                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">Mejora continua</p>
                            </div>
                        </div>
                    </div>

                    {/* Charts Row */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                        {/* Monthly Trend */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">TENDENCIA MENSUAL</h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">Evolución de montos 2024</p>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={monthlyTrend}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid-color)" />
                                    <XAxis dataKey="month" tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} />
                                    <YAxis tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} />
                                    <Tooltip contentStyle={{ backgroundColor: 'var(--chart-tooltip-bg)', color: 'var(--chart-tooltip-text)', borderColor: 'var(--chart-grid-color)' }} />
                                    <Line type="monotone" dataKey="total" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Distribution by Type */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">DISTRIBUCIÓN POR TIPO</h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">Montos por categoría</p>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={distribution}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid-color)" />
                                    <XAxis dataKey="type" tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} />
                                    <YAxis tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} />
                                    <Tooltip contentStyle={{ backgroundColor: 'var(--chart-tooltip-bg)', color: 'var(--chart-tooltip-text)', borderColor: 'var(--chart-grid-color)' }} />
                                    <Bar dataKey="total" fill="#3b82f6" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Bottom Charts Row */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Top Bancos */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">TOP 5 BANCOS EMISORES</h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">Por cantidad de garantías</p>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={kpis?.top_bancos || []} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid-color)" />
                                    <XAxis type="number" tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} />
                                    <YAxis dataKey="nombre" type="category" tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} width={100} />
                                    <Tooltip contentStyle={{ backgroundColor: 'var(--chart-tooltip-bg)', color: 'var(--chart-tooltip-text)', borderColor: 'var(--chart-grid-color)' }} />
                                    <Bar dataKey="total" fill="#10b981" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Top Entidades */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">TOP 5 ENTIDADES PÚBLICAS</h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">Por cantidad de licitaciones</p>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={kpis?.top_entidades || []} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid-color)" />
                                    <XAxis type="number" tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} />
                                    <YAxis dataKey="nombre" type="category" tick={{ fontSize: 12, fill: 'var(--chart-text-color)' }} width={150} />
                                    <Tooltip contentStyle={{ backgroundColor: 'var(--chart-tooltip-bg)', color: 'var(--chart-tooltip-text)', borderColor: 'var(--chart-grid-color)' }} />
                                    <Bar dataKey="total" fill="#f59e0b" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
