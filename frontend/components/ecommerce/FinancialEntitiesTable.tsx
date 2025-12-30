"use client";

import React from "react";

interface FinancialEntitiesTableProps {
    data: Array<{ name: string; garantias: number; monto: number; depts: string; cobertura: string }>;
}

const getEntityColor = (name: string) => {
    const colors = ["bg-blue-600", "bg-indigo-600", "bg-sky-600", "bg-cyan-600", "bg-blue-500", "bg-indigo-500"];
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
};

const getEntityInitials = (name: string) => {
    return name.substring(0, 2).toUpperCase();
};

export const FinancialEntitiesTable: React.FC<FinancialEntitiesTableProps> = ({ data = [] }) => {
    return (
        <div className="rounded-2xl bg-white dark:bg-[#111c44] p-6 shadow-md dark:shadow-xl border border-slate-100 dark:border-white/5 h-full transition-colors duration-300">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Top Entidades Financieras</h3>
                <button className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z" /></svg>
                </button>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-slate-500 dark:text-slate-400">
                    <thead className="bg-slate-50 dark:bg-[#0b122b] text-xs uppercase font-semibold text-slate-500">
                        <tr>
                            <th className="px-4 py-3 rounded-l-lg">Entidad</th>
                            <th className="px-4 py-3 text-center">Garantías</th>
                            <th className="px-4 py-3 text-center">Monto</th>
                            <th className="px-4 py-3 text-center rounded-r-lg">Cobertura</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-700/50">
                        {data.map((entity, index) => (
                            <tr key={index} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                                <td className="px-4 py-3">
                                    <div className="flex items-center gap-3">
                                        <div className={`w-8 h-8 rounded-lg ${getEntityColor(entity.name)} flex items-center justify-center text-white text-[10px] font-bold`}>
                                            {getEntityInitials(entity.name)}
                                        </div>
                                        <div>
                                            <p className="font-semibold text-slate-900 dark:text-white">{entity.name}</p>
                                            <p className="text-[10px] text-slate-500">{entity.depts}</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-4 py-3 text-center font-bold text-slate-900 dark:text-white">{entity.garantias}</td>
                                <td className="px-4 py-3 text-center font-bold text-slate-900 dark:text-white">{new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN', notation: "compact" }).format(entity.monto)}</td>
                                <td className="px-4 py-3 text-center">
                                    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-medium ${entity.cobertura === 'Nacional' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-blue-500/10 text-blue-500 border border-blue-500/20'}`}>
                                        {entity.cobertura}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-700/50">
                <p className="text-xs text-slate-500 dark:text-slate-400">Mostrando {data.length} entidades</p>
            </div>
        </div>
    );
};
