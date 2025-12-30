'use client'

import { TrendingUp, TrendingDown, DollarSign, FileText, Percent } from 'lucide-react'
import { KPIsData } from '@/hooks/use-tendencias'

interface KPICardsProps {
    data?: KPIsData
    isLoading: boolean
}

export function KPICards({ data, isLoading }: KPICardsProps) {
    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value)
    }

    const formatNumber = (value: number) => {
        return new Intl.NumberFormat('es-PE').format(value)
    }

    const kpis = [
        {
            title: 'Total Adjudicado',
            value: data?.total_adjudicado || 0,
            format: formatCurrency,
            icon: DollarSign,
            color: 'bg-blue-500',
            trend: '+12.5%'
        },
        {
            title: 'Cantidad de Procesos',
            value: data?.cantidad_procesos || 0,
            format: formatNumber,
            icon: FileText,
            color: 'bg-purple-500',
            trend: '+8.2%'
        },
        {
            title: 'Ahorro Total',
            value: data?.ahorro_total || 0,
            format: formatCurrency,
            icon: Percent,
            color: 'bg-green-500',
            trend: `${data?.porcentaje_ahorro.toFixed(1)}%`,
            subtitle: `${data?.porcentaje_ahorro.toFixed(1)}% de ahorro`
        }
    ]

    if (isLoading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 animate-pulse">
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
                        <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                        <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
                    </div>
                ))}
            </div>
        )
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {kpis.map((kpi, index) => {
                const Icon = kpi.icon
                const isPositive = kpi.value >= 0

                return (
                    <div
                        key={index}
                        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-6 border border-gray-100 dark:border-gray-700 group hover:-translate-y-1 cursor-default"
                    >
                        <div className="flex items-start justify-between mb-4">
                            <div className="flex-1">
                                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
                                    {kpi.title}
                                </p>
                            </div>
                            <div className={`${kpi.color} p-3 rounded-xl shadow-md group-hover:scale-110 transition-transform duration-300`}>
                                <Icon className="w-6 h-6 text-white" />
                            </div>
                        </div>

                        <div className="mb-2">
                            <h3 className="text-3xl font-bold text-gray-900 dark:text-white">
                                {kpi.format(kpi.value)}
                            </h3>
                        </div>

                        <div className="flex items-center gap-2">
                            {isPositive ? (
                                <TrendingUp className="w-4 h-4 text-green-600" />
                            ) : (
                                <TrendingDown className="w-4 h-4 text-red-600" />
                            )}
                            <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                                {kpi.trend}
                            </span>
                            {kpi.subtitle && (
                                <span className="text-sm text-gray-500 dark:text-gray-400">
                                    {kpi.subtitle}
                                </span>
                            )}
                        </div>
                    </div>
                )
            })}
        </div>
    )
}
