"use client";

import React from "react";
import { Users, Package } from "lucide-react";

interface EcommerceMetricsProps {
    licitaciones?: number;
    monto?: number;
}

export const EcommerceMetrics: React.FC<EcommerceMetricsProps> = ({ licitaciones, monto }) => {
    const formattedMonto = new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN', minimumFractionDigits: 2 }).format(monto || 0);
    const formattedLicitaciones = new Intl.NumberFormat('es-PE').format(licitaciones || 0);

    return (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 h-full">
            {/* Card 1: Licitaciones */}
            <div className="relative overflow-hidden rounded-2xl bg-white dark:bg-[#111c44] p-6 shadow-md dark:shadow-xl border border-slate-100 dark:border-white/5 transition-colors duration-300">
                <div className="flex items-start justify-between">
                    <div className="rounded-xl bg-blue-500/10 p-3">
                        <Users className="h-6 w-6 text-blue-500" />
                    </div>
                </div>
                <div className="mt-4">
                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Licitaciones</p>
                    <h3 className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">{formattedLicitaciones}</h3>
                </div>
            </div>

            {/* Card 2: Monto Adjudicado */}
            <div className="relative overflow-hidden rounded-2xl bg-white dark:bg-[#111c44] p-6 shadow-md dark:shadow-xl border border-slate-100 dark:border-white/5 transition-colors duration-300">
                <div className="flex items-start justify-between">
                    <div className="rounded-xl bg-purple-500/10 p-3">
                        <Package className="h-6 w-6 text-purple-500" />
                    </div>
                </div>
                <div className="mt-4">
                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Monto Adjudicado</p>
                    <h3 className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">{formattedMonto}</h3>
                </div>
            </div>
        </div>
    );
};
