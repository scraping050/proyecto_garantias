'use client'

import { useState } from 'react'
import { ConsortiumData, ConsortiumMember } from '@/hooks/use-tendencias'
import { ChevronDown, ChevronRight, Users, Building2, Percent, Search, X } from 'lucide-react'

interface ConsortiumTreeProps {
    data?: ConsortiumData
    isLoading: boolean
    searchValue: string
    onSearchChange: (value: string) => void
}

export function ConsortiumTree({ data, isLoading, searchValue, onSearchChange }: ConsortiumTreeProps) {
    const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set())

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

    const toggleExpand = (index: number) => {
        const newExpanded = new Set(expandedItems)
        if (newExpanded.has(index)) {
            newExpanded.delete(index)
        } else {
            newExpanded.add(index)
        }
        setExpandedItems(newExpanded)
    }

    if (isLoading) {
        return (
            <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-6 animate-pulse"></div>
                <div className="space-y-3">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="h-16 bg-gray-100 rounded animate-pulse"></div>
                    ))}
                </div>
            </div>
        )
    }

    if (!data || data.data.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Desglose de Consorcios</h3>
                <div className="h-64 flex flex-col items-center justify-center text-gray-500 dark:text-gray-400">
                    <Users className="w-12 h-12 mb-2 text-gray-400 dark:text-gray-500" />
                    <p>No hay consorcios disponibles</p>
                    <p className="text-sm mt-1">Usa el buscador para encontrar consorcios específicos</p>
                </div>
            </div>
        )
    }

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Desglose de Consorcios</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        {data.total} consorcios encontrados
                    </p>
                </div>

                <div className="relative w-full md:w-96">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                        type="text"
                        value={searchValue}
                        onChange={(e) => onSearchChange(e.target.value)}
                        placeholder="Buscar por RUC, nombre, o miembro..."
                        className="w-full pl-9 pr-8 py-2 border border-gray-200 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-gray-50 dark:bg-gray-900 text-sm"
                    />
                    {searchValue && (
                        <button
                            onClick={() => onSearchChange('')}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                            <X className="w-3 h-3" />
                        </button>
                    )}
                </div>
            </div>

            <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {data.data.map((consortium, index) => {
                    const isExpanded = expandedItems.has(index)

                    return (
                        <div
                            key={index}
                            className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden hover:border-blue-300 dark:hover:border-blue-500 transition-colors"
                        >
                            {/* Consortium Header */}
                            <button
                                onClick={() => toggleExpand(index)}
                                className="w-full p-4 bg-gray-50 dark:bg-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-left"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start gap-3 flex-1">
                                        <div className="mt-1">
                                            {isExpanded ? (
                                                <ChevronDown className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                                            ) : (
                                                <ChevronRight className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                                            )}
                                        </div>
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <Building2 className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                                                <h4 className="font-semibold text-gray-900 dark:text-white">
                                                    {consortium.proveedor_ganador}
                                                </h4>
                                            </div>
                                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                                                {consortium.nomenclatura}
                                            </p>
                                            <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                                                <span className="font-mono">{consortium.ruc_ganador}</span>
                                                <span className="flex items-center gap-1">
                                                    <Users className="w-3 h-3" />
                                                    {consortium.cantidad_miembros} miembros
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="text-right ml-4">
                                        <p className="text-sm font-bold text-blue-600 dark:text-blue-400">
                                            {formatCurrency(consortium.monto_adjudicado)}
                                        </p>
                                    </div>
                                </div>
                            </button>

                            {/* Consortium Members */}
                            {isExpanded && (
                                <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
                                    <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                                        <Users className="w-4 h-4" />
                                        Miembros del Consorcio
                                    </h5>
                                    <div className="space-y-2">
                                        {consortium.miembros.map((member, memberIndex) => (
                                            <div
                                                key={memberIndex}
                                                className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg"
                                            >
                                                <div className="flex-1">
                                                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                                                        {member.nombre_miembro}
                                                    </p>
                                                    <p className="text-xs text-gray-600 dark:text-gray-400 font-mono mt-1">
                                                        RUC: {member.ruc_miembro}
                                                    </p>
                                                </div>
                                                <div className="flex items-center gap-2 ml-4">
                                                    <Percent className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                                                    <span className="text-lg font-bold text-blue-700 dark:text-blue-300">
                                                        {member.porcentaje_participacion.toFixed(1)}%
                                                    </span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Verification */}
                                    <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                                        <div className="flex items-center justify-between text-xs">
                                            <span className="text-gray-600 dark:text-gray-400">Total Participación:</span>
                                            <span className={`font-bold ${Math.abs(consortium.miembros.reduce((sum, m) => sum + m.porcentaje_participacion, 0) - 100) < 0.1
                                                ? 'text-green-600 dark:text-green-400'
                                                : 'text-red-600 dark:text-red-400'
                                                }`}>
                                                {consortium.miembros.reduce((sum, m) => sum + m.porcentaje_participacion, 0).toFixed(1)}%
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
