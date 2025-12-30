'use client'

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { SavingsGaugeData } from '@/hooks/use-tendencias'
import { TrendingUp, TrendingDown, DollarSign } from 'lucide-react'

interface SavingsGaugeProps {
    data?: SavingsGaugeData
    isLoading: boolean
}

export function SavingsGauge({ data, isLoading }: SavingsGaugeProps) {
    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value)
    }

    if (isLoading) {
        return (
            <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-6 animate-pulse"></div>
                <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
            </div>
        )
    }

    if (!data) {
        return (
            <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Termómetro de Ahorro</h3>
                <div className="h-64 flex items-center justify-center text-gray-500">
                    No hay datos disponibles
                </div>
            </div>
        )
    }

    const chartData = [
        { name: 'Adjudicado', value: data.monto_adjudicado, color: '#3b82f6' },
        { name: 'Ahorro', value: data.ahorro > 0 ? data.ahorro : 0, color: '#10b981' }
    ]

    const getStatusColor = () => {
        switch (data.status) {
            case 'good':
                return 'text-green-600 bg-green-50'
            case 'moderate':
                return 'text-yellow-600 bg-yellow-50'
            case 'over_budget':
                return 'text-red-600 bg-red-50'
            default:
                return 'text-gray-600 bg-gray-50'
        }
    }

    const getStatusText = () => {
        switch (data.status) {
            case 'good':
                return 'Excelente Ahorro'
            case 'moderate':
                return 'Ahorro Moderado'
            case 'over_budget':
                return 'Sobre Presupuesto'
            default:
                return 'Sin Datos'
        }
    }

    return (
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">Termómetro de Ahorro</h3>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor()}`}>
                    {getStatusText()}
                </span>
            </div>

            <div className="mb-6">
                <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                        <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            paddingAngle={5}
                            dataKey="value"
                        >
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Pie>
                        <Tooltip
                            formatter={(value: number) => formatCurrency(value)}
                            contentStyle={{
                                backgroundColor: 'white',
                                border: '1px solid #e5e7eb',
                                borderRadius: '8px',
                                padding: '12px'
                            }}
                        />
                    </PieChart>
                </ResponsiveContainer>

                <div className="text-center -mt-4">
                    <p className="text-3xl font-bold text-gray-900">
                        {data.porcentaje_ahorro.toFixed(1)}%
                    </p>
                    <p className="text-sm text-gray-500">Porcentaje de Ahorro</p>
                </div>
            </div>

            <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-2">
                        <DollarSign className="w-5 h-5 text-gray-600" />
                        <span className="text-sm font-medium text-gray-700">Monto Referencial</span>
                    </div>
                    <span className="text-sm font-bold text-gray-900">
                        {formatCurrency(data.monto_referencial)}
                    </span>
                </div>

                <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center gap-2">
                        <DollarSign className="w-5 h-5 text-blue-600" />
                        <span className="text-sm font-medium text-blue-700">Monto Adjudicado</span>
                    </div>
                    <span className="text-sm font-bold text-blue-900">
                        {formatCurrency(data.monto_adjudicado)}
                    </span>
                </div>

                <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center gap-2">
                        {data.ahorro >= 0 ? (
                            <TrendingUp className="w-5 h-5 text-green-600" />
                        ) : (
                            <TrendingDown className="w-5 h-5 text-red-600" />
                        )}
                        <span className="text-sm font-medium text-green-700">Ahorro Total</span>
                    </div>
                    <span className={`text-sm font-bold ${data.ahorro >= 0 ? 'text-green-900' : 'text-red-900'}`}>
                        {formatCurrency(Math.abs(data.ahorro))}
                    </span>
                </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200 text-center">
                <p className="text-xs text-gray-500">
                    Basado en {data.cantidad_procesos.toLocaleString('es-PE')} procesos
                </p>
            </div>
        </div>
    )
}
