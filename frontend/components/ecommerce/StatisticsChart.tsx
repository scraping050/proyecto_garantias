"use client";

import React from "react";
import dynamic from "next/dynamic";
import { ApexOptions } from "apexcharts";

const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

export const StatisticsChart: React.FC = () => {
    const options: ApexOptions = {
        chart: { type: "donut" },
        labels: ["Obras", "Servicios", "Bienes", "Consultoría"],
        colors: ["#6366F1", "#10B981", "#F59E0B", "#EF4444"],
        plotOptions: {
            pie: {
                donut: {
                    size: "65%",
                    labels: {
                        show: true,
                        name: { show: true, fontSize: "14px", fontFamily: "Inter, sans-serif", color: "#64748B" },
                        value: { show: true, fontSize: "24px", fontFamily: "Inter, sans-serif", fontWeight: 600, color: "#1E293B" },
                        total: { show: true, label: "Total", color: "#64748B", formatter: () => "425" }
                    }
                }
            }
        },
        dataLabels: { enabled: false },
        legend: { position: "bottom", horizontalAlign: "center", itemMargin: { horizontal: 10 } },
        stroke: { show: false },
        tooltip: { theme: 'dark' }
    };

    const series = [150, 200, 50, 25];

    return (
        <div className="rounded-2xl border border-slate-200/60 bg-white/50 p-6 shadow-lg shadow-slate-200/50 dark:border-slate-700/60 dark:bg-slate-800/50 dark:shadow-none bg-backdrop-blur-xl h-full">
            <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Distribución por Categoría</h3>
                <select className="rounded-lg border-0 bg-slate-100 py-1 pl-3 pr-8 text-xs font-semibold text-slate-600 focus:ring-2 focus:ring-indigo-500 dark:bg-slate-700 dark:text-slate-300">
                    <option>Este Mes</option>
                    <option>Este Año</option>
                </select>
            </div>
            <div className="flex items-center justify-center">
                <div className="h-80 w-full">
                    <ReactApexChart options={options} series={series} type="donut" height={320} />
                </div>
            </div>
        </div>
    );
};
