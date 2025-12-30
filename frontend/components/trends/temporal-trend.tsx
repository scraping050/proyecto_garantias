'use client'

import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { TemporalTrendData } from '@/hooks/use-tendencias'

interface TemporalTrendProps {
    data?: TemporalTrendData
    isLoading: boolean
}

export function TemporalTrend({ data, isLoading }: TemporalTrendProps) {
    const formatCurrency = (value: number) => {
        if (value >= 1_000_000_000) {
            return `S/ ${(value / 1_000_000_000).toFixed(1)} mil millones`
        }
        if (value >= 1_000_000) {
            return `S/ ${(value / 1_000_000).toFixed(1)}M`
        }
        return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            notation: 'compact',
            maximumFractionDigits: 1
        }).format(value)
    }

    if (isLoading) {
        return (
            <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-6 animate-pulse"></div>
                <div className="h-80 bg-gray-100 rounded animate-pulse"></div>
            </div>
        )
    }

    if (!data || data.data.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Tendencia Temporal de Gastos</h3>
                <div className="h-80 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    No hay datos disponibles
                </div>
            </div>
        )
    }

    const totalAmount = data.data.reduce((sum, item) => sum + item.monto_total, 0)
    const avgMonthly = totalAmount / data.data.length

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Tendencia Temporal de Gastos</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Año {data.year}</p>
                </div>
                <div className="text-right">
                    <p className="text-sm text-gray-600 dark:text-gray-300">Promedio Mensual</p>
                    <p className="text-lg font-bold text-blue-600 dark:text-blue-400">{formatCurrency(avgMonthly)}</p>
                </div>
            </div>

            <ResponsiveContainer width="100%" height={320}>
                <AreaChart
                    data={data.data}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                    <defs>
                        <linearGradient id="colorMonto" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis
                        dataKey="month"
                        stroke="#6b7280"
                        style={{ fontSize: '12px' }}
                    />
                    <YAxis
                        tickFormatter={formatCurrency}
                        stroke="#6b7280"
                        style={{ fontSize: '12px' }}
                    />
                    <Tooltip
                        formatter={(value: number) => [formatCurrency(value), 'Monto']}
                        contentStyle={{
                            backgroundColor: 'var(--background)',
                            borderColor: 'var(--border)',
                            color: 'var(--foreground)',
                            borderRadius: '8px',
                            padding: '12px'
                        }}
                        labelStyle={{ fontWeight: 'bold', marginBottom: '8px', color: 'var(--foreground)' }}
                    />
                    <Area
                        type="monotone"
                        dataKey="monto_total"
                        stroke="#3b82f6"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorMonto)"
                    />
                </AreaChart>
            </ResponsiveContainer>

            <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                    <p className="text-gray-600 dark:text-gray-300 mb-1">Total Año</p>
                    <p className="text-lg font-bold text-blue-700 dark:text-blue-400">
                        {formatCurrency(totalAmount)}
                    </p>
                </div>
                <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-3">
                    <p className="text-gray-600 dark:text-gray-300 mb-1">Meses con Datos</p>
                    <p className="text-lg font-bold text-green-700 dark:text-green-400">
                        {data.data.length}
                    </p>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3">
                    <p className="text-gray-600 dark:text-gray-300 mb-1">Total Procesos</p>
                    <p className="text-lg font-bold text-purple-700 dark:text-purple-400">
                        {data.data.reduce((sum, item) => sum + item.cantidad, 0).toLocaleString('es-PE')}
                    </p>
                </div>
            </div>
        </div>
    )
}
