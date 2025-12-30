'use client'

import { GeographicData } from '@/hooks/use-tendencias'
import { MapPin, ArrowLeft } from 'lucide-react'

interface GeographicHeatmapProps {
    data?: GeographicData
    isLoading: boolean
    onDrillDown?: (location: string) => void
    onDrillUp?: () => void
}

export function GeographicHeatmap({ data, isLoading, onDrillDown, onDrillUp }: GeographicHeatmapProps) {
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
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Mapa de Calor de Inversión Pública</h3>
                <div className="h-96 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    No hay datos disponibles
                </div>
            </div>
        )
    }

    // Calculate color intensity based on monto_total
    const maxMonto = Math.max(...data.data.map(d => d.monto_total))
    const minMonto = Math.min(...data.data.map(d => d.monto_total))

    const getColorIntensity = (monto: number) => {
        if (maxMonto === minMonto) return 0.5
        return (monto - minMonto) / (maxMonto - minMonto)
    }

    const getColorClass = (intensity: number) => {
        // Paleta personalizada: Indigo → Azul Cobalto → Azul Marino → Azul Oxford
        if (intensity > 0.8) return {
            bg: 'bg-gradient-to-br from-[#002147] to-[#001833]',  // Azul Oxford (muy oscuro)
            hover: 'hover:from-[#003366] hover:to-[#002147]',
            text: 'text-white',
            shadow: 'drop-shadow-[0_1px_2px_rgba(0,0,0,0.5)]'
        }
        if (intensity > 0.6) return {
            bg: 'bg-gradient-to-br from-[#000080] to-[#00008B]',  // Azul Marino
            hover: 'hover:from-[#0F2C4A] hover:to-[#000080]',
            text: 'text-white',
            shadow: 'drop-shadow-[0_1px_2px_rgba(0,0,0,0.4)]'
        }
        if (intensity > 0.4) return {
            bg: 'bg-gradient-to-br from-[#0047AB] to-[#0051BA]',  // Azul Cobalto
            hover: 'hover:from-[#0056D2] hover:to-[#0047AB]',
            text: 'text-white',
            shadow: 'drop-shadow-[0_1px_2px_rgba(0,0,0,0.3)]'
        }
        if (intensity > 0.2) return {
            bg: 'bg-gradient-to-br from-blue-400 to-blue-500',  // Azul Medio
            hover: 'hover:from-blue-300 hover:to-blue-400',
            text: 'text-white',
            shadow: 'drop-shadow-[0_1px_2px_rgba(0,0,0,0.2)]'
        }
        return {
            bg: 'bg-gradient-to-br from-indigo-300 to-indigo-400',  // Indigo claro
            hover: 'hover:from-indigo-200 hover:to-indigo-300',
            text: 'text-gray-900',
            shadow: 'drop-shadow-[0_1px_1px_rgba(255,255,255,0.9)]'
        }
    }

    // Sort by monto_total descending
    const sortedData = [...data.data].sort((a, b) => b.monto_total - a.monto_total)

    return (
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    {data.parent && (
                        <button
                            onClick={onDrillUp}
                            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-all duration-200 hover:shadow-md hover:-translate-y-0.5"
                            title="Volver a vista de departamentos"
                        >
                            <ArrowLeft className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                        </button>
                    )}
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-md">
                            <MapPin className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                                Mapa de Calor de Inversión Pública
                            </h3>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                {data.level === 'departamento' ? 'Vista por Departamento' : `Provincias de ${data.parent}`}
                            </p>
                        </div>
                    </div>
                </div>
                <div className="text-right bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-700 dark:to-gray-600 rounded-xl p-4 border border-blue-200 dark:border-gray-500">
                    <p className="text-sm font-semibold text-gray-600 dark:text-gray-200 uppercase tracking-wide">Total Invertido</p>
                    <p className="text-2xl font-black text-blue-600 dark:text-blue-300 mt-1">
                        {formatCurrency(data.data.reduce((sum, d) => sum + d.monto_total, 0))}
                    </p>
                </div>
            </div>

            {/* Grid-based heat map */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-6">
                {sortedData.map((item, index) => {
                    const intensity = getColorIntensity(item.monto_total)
                    const colors = getColorClass(intensity)
                    const canDrillDown = data.level === 'departamento' && onDrillDown

                    return (
                        <button
                            key={index}
                            onClick={() => canDrillDown && onDrillDown(item.location)}
                            disabled={!canDrillDown}
                            className={`${colors.bg} ${colors.hover} ${colors.text} ${canDrillDown ? 'cursor-pointer' : 'cursor-default'
                                } rounded-xl p-5 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl border-2 border-white/30 relative overflow-hidden group`}
                        >
                            {/* Efecto de brillo al hover */}
                            <div className="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                            <div className="relative z-10">
                                <div className="flex items-start justify-between mb-3">
                                    <MapPin className={`w-5 h-5 ${colors.shadow}`} />
                                    {canDrillDown && (
                                        <span className={`text-xs font-semibold px-2 py-1 bg-black/20 rounded-full ${colors.shadow}`}>
                                            Ver detalles
                                        </span>
                                    )}
                                </div>
                                <h4 className={`font-black text-base mb-2 text-left ${colors.shadow} leading-tight`}>
                                    {item.location}
                                </h4>
                                <p className={`text-sm font-bold mb-1 text-left ${colors.shadow}`}>
                                    {formatCurrency(item.monto_total)}
                                </p>
                                <p className={`text-xs font-semibold text-left ${colors.shadow} opacity-90`}>
                                    {item.cantidad_procesos} procesos
                                </p>
                            </div>
                        </button>
                    )
                })}
            </div>

            {/* Legend mejorada */}
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-6 border-t-2 border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Menor inversión</span>
                    <div className="flex gap-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-indigo-300 to-indigo-400 rounded-lg shadow-md border border-white"></div>
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-500 rounded-lg shadow-md border border-white"></div>
                        <div className="w-8 h-8 bg-gradient-to-br from-[#0047AB] to-[#0051BA] rounded-lg shadow-md border border-white"></div>
                        <div className="w-8 h-8 bg-gradient-to-br from-[#000080] to-[#00008B] rounded-lg shadow-md border border-white"></div>
                        <div className="w-8 h-8 bg-gradient-to-br from-[#002147] to-[#001833] rounded-lg shadow-md border border-white"></div>
                    </div>
                    <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Mayor inversión</span>
                </div>
                <div className="flex items-center gap-2 text-sm bg-gray-100 dark:bg-gray-700 px-4 py-2 rounded-xl">
                    <div className="w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full animate-pulse"></div>
                    <span className="font-bold text-gray-700 dark:text-gray-200">
                        {data.data.length} {data.level === 'departamento' ? 'departamentos' : 'provincias'}
                    </span>
                </div>
            </div>
        </div>
    )
}
