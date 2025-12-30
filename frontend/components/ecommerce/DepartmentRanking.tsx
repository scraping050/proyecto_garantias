"use client";

import React from "react";
import Image from "next/image";

interface DepartmentRankingProps {
    data: Array<{ rank: number; name: string; count: number; percentage: number }>;
}

export const DepartmentRanking: React.FC<DepartmentRankingProps> = ({ data = [] }) => {
    return (
        <div className="rounded-2xl bg-white dark:bg-[#111c44] p-6 shadow-md dark:shadow-xl border border-slate-100 dark:border-white/5 h-full flex flex-col transition-colors duration-300">
            {/* Header */}
            <div className="flex justify-between items-center mb-2">
                <div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Licitaciones por Departamento</h3>
                    <p className="text-sm text-slate-500 dark:text-slate-400">Distribución de licitaciones en Perú</p>
                </div>
                <button className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z" />
                    </svg>
                </button>
            </div>

            {/* Map of Peru - Transparent Image */}
            <div className="h-80 w-full bg-slate-50 dark:bg-[#0b122b]/50 rounded-2xl flex items-center justify-center mb-6 p-1 transition-colors duration-300 overflow-hidden">
                <img
                    src="/peru-map-transparent.png"
                    alt="Mapa de Perú detallado por departamentos"
                    className="w-full h-full object-contain drop-shadow-sm dark:drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]"
                />
            </div>

            {/* Ranking List */}
            <div className="flex-1 overflow-y-auto space-y-4 max-h-[400px]">
                {data.slice(0, 10).map((dept) => (
                    <div key={dept.rank} className="group">
                        <div className="flex items-center gap-3 mb-2">
                            {/* Rank Badge */}
                            <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-blue-500 text-white flex items-center justify-center font-bold text-sm">
                                #{dept.rank}
                            </div>

                            {/* Department Info */}
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wide">
                                    {dept.name}
                                </p>
                                <p className="text-xs text-slate-500 dark:text-slate-400">
                                    {new Intl.NumberFormat('es-PE').format(dept.count)} Licitaciones
                                </p>
                            </div>

                            {/* Percentage */}
                            <span className="text-lg font-bold text-slate-900 dark:text-white flex-shrink-0">
                                {dept.percentage}%
                            </span>
                        </div>

                        {/* Progress Bar */}
                        <div className="h-2 w-full bg-slate-200 dark:bg-slate-700/50 rounded-full overflow-hidden ml-13">
                            <div
                                className="h-full bg-blue-600 rounded-full transition-all duration-500"
                                style={{ width: `${Math.min(dept.percentage, 100)}%` }}
                            />
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer */}
            <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700/50">
                <p className="text-xs text-slate-500 dark:text-slate-400">
                    Mostrando {Math.min(data.length, 10)} departamentos
                </p>
            </div>
        </div>
    );
};
