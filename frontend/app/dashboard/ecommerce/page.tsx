"use client";

import React from "react";
import { Search, Bell, Menu } from "lucide-react";
import { EcommerceMetrics } from "@/components/ecommerce/EcommerceMetrics";
import { DistributionRadialChart } from "@/components/ecommerce/DistributionRadialChart";
import { StatusChart } from "@/components/ecommerce/StatusChart";
import { SalesAreaChart } from "@/components/ecommerce/SalesAreaChart";
import { DepartmentRanking } from "@/components/ecommerce/DepartmentRanking";
import { FinancialEntitiesTable } from "@/components/ecommerce/FinancialEntitiesTable";

export default function EcommerceDashboardPage() {
    return (
        <div className="min-h-screen bg-[#0b122b] p-4 text-slate-200 font-sans">
            <div className="mx-auto max-w-[1600px] space-y-6">

                {/* Top Bar (Mockup Style) */}
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-4">
                        <button className="p-2 rounded-lg bg-[#111c44] text-slate-400 hover:text-white">
                            <Menu className="h-5 w-5" />
                        </button>
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                            <input
                                type="text"
                                placeholder="Buscar o escribir comando..."
                                className="h-10 w-64 rounded-full bg-[#111c44] pl-10 pr-4 text-sm text-slate-300 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                            />
                            <span className="absolute right-3 top-1/2 -translate-y-1/2 rounded bg-slate-700/50 px-1.5 py-0.5 text-[10px] font-mono text-slate-400">⌘K</span>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <button className="p-2 rounded-full hover:bg-[#111c44] text-slate-400">
                            <Bell className="h-5 w-5" />
                        </button>
                        <div className="flex items-center gap-2">
                            <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-xs font-bold text-white">MQ</div>
                        </div>
                    </div>
                </div>

                {/* --- ROW 1: Metrics + Radial Distribution --- */}
                <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
                    {/* Metrics (Licitaciones & Monto) - Spans 6 cols (3 each inside component) */}
                    <div className="lg:col-span-8">
                        <EcommerceMetrics />
                    </div>

                    {/* Distribution Radial - Spans 4 cols */}
                    <div className="lg:col-span-4 h-full">
                        <DistributionRadialChart />
                    </div>
                </div>

                {/* --- ROW 2: Status Chart --- */}
                <div className="w-full">
                    <StatusChart />
                </div>

                {/* --- ROW 3: Monthly Statistics Area Chart --- */}
                <div className="w-full">
                    <SalesAreaChart />
                </div>

                {/* --- ROW 4: Department Ranking + Financial Entities --- */}
                <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
                    {/* Department Ranking - 4 cols */}
                    <div className="lg:col-span-4">
                        <DepartmentRanking />
                    </div>
                    {/* Financial Entities Table - 8 cols */}
                    <div className="lg:col-span-8">
                        <FinancialEntitiesTable />
                    </div>
                </div>

            </div>
        </div>
    );
}
