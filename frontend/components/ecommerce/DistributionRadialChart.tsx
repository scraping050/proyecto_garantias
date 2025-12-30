"use client";

import React from "react";
import dynamic from "next/dynamic";
import { ApexOptions } from "apexcharts";
import { TrendingUp } from "lucide-react";

const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

interface DistributionRadialChartProps {
    data: Array<{ type: string, total: number }>;
}

export const DistributionRadialChart: React.FC<DistributionRadialChartProps> = ({ data = [] }) => {
    const totalAmount = data.reduce((sum, item) => sum + item.total, 0);

    const categories = [
        { key: "BIENES", label: "Bien", color: "#3B82F6", textColor: "text-blue-600" },
        { key: "SERVICIOS", label: "Servicio", color: "#10B981", textColor: "text-emerald-600" },
        { key: "OBRAS", label: "Obra", color: "#F59E0B", textColor: "text-amber-600" }
    ];

    const stats = categories.map(cat => {
        const item = data.find(d => d.type.toUpperCase().includes(cat.key) || cat.key.includes(d.type.toUpperCase()));
        const value = item ? item.total : 0;
        const percent = totalAmount > 0 ? (value / totalAmount * 100) : 0;

        return {
            label: cat.label,
            value: value,
            valueFormatted: new Intl.NumberFormat('es-PE').format(value),
            percent: percent.toFixed(2),
            color: cat.color,
            textColor: cat.textColor
        };
    });

    // Calcular porcentajes para el gráfico (solo los que tienen valores)
    const chartPercentages = stats.map(s => parseFloat(s.percent));

    const options: ApexOptions = {
        chart: {
            type: "radialBar",
            sparkline: { enabled: false }
        },
        plotOptions: {
            radialBar: {
                startAngle: -90,
                endAngle: 90,
                track: {
                    background: "#E5E7EB",
                    strokeWidth: '100%',
                    margin: 8
                },
                hollow: {
                    size: '60%'
                },
                dataLabels: {
                    name: {
                        show: true,
                        fontSize: '14px',
                        color: '#64748B',
                        offsetY: -10
                    },
                    value: {
                        show: true,
                        fontSize: '32px',
                        fontWeight: 700,
                        color: '#1E293B',
                        offsetY: 5,
                        formatter: () => "100%"
                    },
                    total: {
                        show: true,
                        label: "Total",
                        fontSize: '14px',
                        color: "#64748B",
                        formatter: () => "100%"
                    }
                }
            }
        },
        colors: stats.map(s => s.color),
        stroke: {
            lineCap: "round"
        },
        labels: stats.map(s => s.label)
    };

    return (
        <div className="rounded-2xl bg-white dark:bg-[#111c44] p-6 shadow-md dark:shadow-xl border border-slate-100 dark:border-white/5 h-full flex flex-col transition-colors duration-300">
            {/* Header */}
            <div className="flex justify-between items-start mb-1">
                <div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Distribución por Tipo</h3>
                    <p className="text-sm text-slate-500 dark:text-slate-400">Licitaciones por categoría</p>
                </div>
                <button className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z" />
                    </svg>
                </button>
            </div>

            {/* Chart */}
            <div className="flex items-center justify-center my-4">
                <ReactApexChart
                    options={options}
                    series={chartPercentages}
                    type="radialBar"
                    height={280}
                    width="100%"
                />
            </div>

            {/* Description Text */}
            <div className="text-center text-sm text-slate-600 dark:text-slate-400 mb-4 px-2">
                {new Intl.NumberFormat('es-PE').format(totalAmount)} licitaciones distribuidas: {
                    stats.map((stat, idx) => (
                        <React.Fragment key={idx}>
                            <span className="font-medium text-slate-700 dark:text-slate-300">
                                {stat.label.toUpperCase()}
                            </span> ({stat.percent}%){idx < stats.length - 1 ? ', ' : '.'}
                        </React.Fragment>
                    ))
                }
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-3 bg-slate-50 dark:bg-[#0b122b] rounded-xl p-4">
                {stats.map((stat, i) => (
                    <div key={i} className="text-center">
                        <p className={`text-sm font-semibold ${stat.textColor} mb-1`}>
                            {stat.label}
                        </p>
                        <div className="flex items-center justify-center gap-1">
                            <p className="text-xl font-bold text-slate-900 dark:text-white">
                                {stat.valueFormatted}
                            </p>
                            <TrendingUp className="w-4 h-4 text-green-500" />
                        </div>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                            {stat.percent}%
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};
