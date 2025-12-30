'use client'

import { useState } from 'react'
import { TopProvidersData } from '@/hooks/use-tendencias'
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react'

interface TopProvidersTableProps {
    data?: TopProvidersData
    isLoading: boolean
}

type SortField = 'proveedor' | 'monto_total' | 'cantidad_contratos'
type SortDirection = 'asc' | 'desc'

export function TopProvidersTable({ data, isLoading }: TopProvidersTableProps) {
    const [sortField, setSortField] = useState<SortField>('monto_total')
    const [sortDirection, setSortDirection] = useState<SortDirection>('desc')

    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value)
    }

    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
        } else {
            setSortField(field)
            setSortDirection('desc')
        }
    }

    const getSortIcon = (field: SortField) => {
        if (sortField !== field) {
            return <ArrowUpDown className="w-4 h-4 text-gray-400" />
        }
        return sortDirection === 'asc' ? (
            <ArrowUp className="w-4 h-4 text-blue-600" />
        ) : (
            <ArrowDown className="w-4 h-4 text-blue-600" />
        )
    }

    if (isLoading) {
        return (
            <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-6 animate-pulse"></div>
                <div className="space-y-3">
                    {[1, 2, 3, 4, 5].map((i) => (
                        <div key={i} className="h-12 bg-gray-100 rounded animate-pulse"></div>
                    ))}
                </div>
            </div>
        )
    }

    if (!data || data.data.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Top Proveedores Ganadores</h3>
                <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    No hay datos disponibles
                </div>
            </div>
        )
    }

    const sortedData = [...data.data].sort((a, b) => {
        const aValue = a[sortField]
        const bValue = b[sortField]

        if (typeof aValue === 'string' && typeof bValue === 'string') {
            return sortDirection === 'asc'
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue)
        }

        return sortDirection === 'asc'
            ? (aValue as number) - (bValue as number)
            : (bValue as number) - (aValue as number)
    })

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Top Proveedores Ganadores</h3>
                <span className="text-sm text-gray-500 dark:text-gray-400">Top {data.data.length} proveedores</span>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="border-b border-gray-200 dark:border-gray-700">
                            <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                                <button
                                    onClick={() => handleSort('proveedor')}
                                    className="flex items-center gap-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                                >
                                    Proveedor
                                    {getSortIcon('proveedor')}
                                </button>
                            </th>
                            <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                                RUC
                            </th>
                            <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                                <button
                                    onClick={() => handleSort('monto_total')}
                                    className="flex items-center gap-2 ml-auto hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                                >
                                    Monto Total
                                    {getSortIcon('monto_total')}
                                </button>
                            </th>
                            <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                                <button
                                    onClick={() => handleSort('cantidad_contratos')}
                                    className="flex items-center gap-2 mx-auto hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                                >
                                    Contratos
                                    {getSortIcon('cantidad_contratos')}
                                </button>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((provider, index) => (
                            <tr
                                key={index}
                                className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                            >
                                <td className="py-3 px-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-700 dark:text-blue-400 font-bold text-sm">
                                            {index + 1}
                                        </div>
                                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                                            {provider.proveedor}
                                        </span>
                                    </div>
                                </td>
                                <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400 font-mono">
                                    {provider.ruc}
                                </td>
                                <td className="py-3 px-4 text-right text-sm font-semibold text-gray-900 dark:text-white">
                                    {formatCurrency(provider.monto_total)}
                                </td>
                                <td className="py-3 px-4 text-center">
                                    <span className="inline-flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
                                        {provider.cantidad_contratos}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                        <p className="text-gray-600 dark:text-gray-300 mb-1">Total Adjudicado</p>
                        <p className="text-lg font-bold text-blue-700 dark:text-blue-400">
                            {formatCurrency(data.data.reduce((sum, p) => sum + p.monto_total, 0))}
                        </p>
                    </div>
                    <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-3">
                        <p className="text-gray-600 dark:text-gray-300 mb-1">Total Contratos</p>
                        <p className="text-lg font-bold text-purple-700 dark:text-purple-400">
                            {data.data.reduce((sum, p) => sum + p.cantidad_contratos, 0).toLocaleString('es-PE')}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
