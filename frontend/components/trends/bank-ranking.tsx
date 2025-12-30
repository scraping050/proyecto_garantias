'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { BankRankingData } from '@/hooks/use-tendencias'

interface BankRankingProps {
    data?: BankRankingData
    isLoading: boolean
}

const COLORS = ['#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#c026d3', '#d946ef', '#e879f9', '#f0abfc', '#f5d0fe', '#fae8ff']

export function BankRanking({ data, isLoading }: BankRankingProps) {
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
                <div className="h-96 bg-gray-100 rounded animate-pulse"></div>
            </div>
        )
    }

    if (!data || data.data.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Ranking de Bancos Garantes</h3>
                <div className="h-96 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    No hay datos disponibles
                </div>
            </div>
        )
    }

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Ranking de Bancos Garantes</h3>
                <span className="text-sm text-gray-500 dark:text-gray-400">Top {data.data.length} bancos</span>
            </div>

            <ResponsiveContainer width="100%" height={400}>
                <BarChart
                    data={data.data}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis
                        type="number"
                        tickFormatter={formatCurrency}
                        stroke="#6b7280"
                        style={{ fontSize: '12px' }}
                    />
                    <YAxis
                        type="category"
                        dataKey="banco"
                        width={180}
                        stroke="#6b7280"
                        style={{ fontSize: '11px' }}
                        interval={0}
                    />
                    <Tooltip
                        formatter={(value: number) => formatCurrency(value)}
                        contentStyle={{
                            backgroundColor: 'var(--background)',
                            borderColor: 'var(--border)',
                            color: 'var(--foreground)',
                            borderRadius: '8px',
                            padding: '12px'
                        }}
                        labelStyle={{ fontWeight: 'bold', marginBottom: '8px', color: 'var(--foreground)' }}
                    />
                    <Bar dataKey="monto_total" radius={[0, 8, 8, 0]}>
                        {data.data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                    <p className="text-gray-600 dark:text-gray-300 mb-1">Total Garantías</p>
                    <p className="text-lg font-bold text-blue-700 dark:text-blue-400">
                        {data.data.reduce((sum, item) => sum + item.cantidad_garantias, 0).toLocaleString('es-PE')}
                    </p>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3">
                    <p className="text-gray-600 dark:text-gray-300 mb-1">Monto Total</p>
                    <p className="text-lg font-bold text-purple-700 dark:text-purple-400">
                        {formatCurrency(data.data.reduce((sum, item) => sum + item.monto_total, 0))}
                    </p>
                </div>
            </div>
        </div>
    )
}
