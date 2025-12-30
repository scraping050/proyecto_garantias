"use client";

import React from "react";
import dynamic from "next/dynamic";
import { ApexOptions } from "apexcharts";

const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

export const TopEntidadesFinancieras: React.FC = () => {
    const options: ApexOptions = {
        chart: { type: "bar", toolbar: { show: false } },
        plotOptions: { bar: { borderRadius: 4, horizontal: true, barHeight: '60%' } },
        colors: ["#3B82F6"],
        xaxis: {
            categories: ["BCP", "BBVA", "Scotiabank", "Interbank", "Mapfre", "Positiva", "Rimac", "Crediscotia"],
            axisBorder: { show: false },
            labels: { style: { colors: "#64748B" } }
        },
        yaxis: { labels: { style: { colors: "#64748B" } } },
        grid: { show: false },
        dataLabels: { enabled: true, textAnchor: 'start', style: { colors: ['#fff'] }, formatter: function (val, opt) { return val + "%" }, offsetX: 0, },
        tooltip: { theme: 'dark', y: { formatter: (val) => `${val}% participación` } }
    };

    const series = [{ name: "Participación", data: [25, 20, 15, 12, 10, 8, 6, 4] }];

    return (
        <div className="rounded-2xl border border-slate-200/60 bg-white/50 p-6 shadow-lg shadow-slate-200/50 dark:border-slate-700/60 dark:bg-slate-800/50 dark:shadow-none bg-backdrop-blur-xl">
            <h3 className="mb-4 text-lg font-bold text-slate-900 dark:text-white">Top Entidades Financieras</h3>
            <div className="h-80 w-full">
                <ReactApexChart options={options} series={series} type="bar" height={320} />
            </div>
        </div>
    );
}
