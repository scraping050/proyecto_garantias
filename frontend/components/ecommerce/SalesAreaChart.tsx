"use client";

import React from "react";
import dynamic from "next/dynamic";
import { ApexOptions } from "apexcharts";

const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

interface SalesAreaChartProps {
    data: Array<{ month: string; total: number }>;
    selectedYear: number;
    onYearChange: (year: number) => void;
}

export const SalesAreaChart: React.FC<SalesAreaChartProps> = ({ data = [], selectedYear, onYearChange }) => {
    const categories = data.map(item => item.month);
    const seriesData = data.map(item => item.total);

    const options: ApexOptions = {
        chart: { type: "area", toolbar: { show: false }, background: 'transparent' },
        stroke: { curve: "smooth", width: 2 },
        colors: ["#3B82F6"], // Blue primary
        fill: {
            type: "gradient",
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.6,
                opacityTo: 0.1,
                stops: [0, 100]
            }
        },
        xaxis: {
            categories: categories,
            axisBorder: { show: false },
            axisTicks: { show: false },
            labels: { style: { colors: "#64748B", fontSize: '12px' } }
        },
        yaxis: {
            labels: { style: { colors: "#64748B" } },
            grid: { show: true, borderColor: '#334155' } // We keep a neutral grid color or use variable if needed
        },
        grid: { borderColor: "#334155", strokeDashArray: 4, show: true, xaxis: { lines: { show: false } } },
        dataLabels: { enabled: false },
        tooltip: { theme: 'dark' },
    };

    const series = [
        { name: "Licitaciones", data: seriesData },
    ];

    const years = [2024, 2025, 2026];

    return (
        <div className="rounded-2xl bg-white dark:bg-[#111c44] p-6 shadow-md dark:shadow-xl border border-slate-100 dark:border-white/5 transition-colors duration-300">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Estadísticas</h3>
                    <p className="text-sm text-slate-500 dark:text-slate-400">Total de licitaciones por mes</p>
                </div>
                <div className="flex bg-slate-100 dark:bg-[#0b122b] rounded-lg p-1">
                    {years.map(year => (
                        <button
                            key={year}
                            onClick={() => onYearChange(year)}
                            className={`px-4 py-1 text-xs font-semibold rounded-md transition-all ${selectedYear === year
                                    ? 'bg-blue-600 text-white shadow-lg'
                                    : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                                }`}
                        >
                            {year}
                        </button>
                    ))}
                </div>
            </div>
            <div className="h-72 w-full">
                <ReactApexChart options={options} series={series} type="area" height={280} />
            </div>
        </div>
    );
};
