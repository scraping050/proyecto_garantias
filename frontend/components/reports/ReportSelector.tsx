"use client";

import React from "react";
import type { ReportType } from "@/types/licitacion";

interface Props {
    selectedType: ReportType;
    onTypeChange: (type: ReportType) => void;
}

export const ReportSelector: React.FC<Props> = ({ selectedType, onTypeChange }) => {
    const options: { id: ReportType; label: string; icon: React.ReactNode; desc: string }[] = [
        {
            id: "entidad",
            label: "Entidad Financiera",
            desc: "Análisis por bancos y aseguradoras",
            icon: (
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
            ),
        },
        {
            id: "departamento",
            label: "Departamento",
            desc: "Distribución geográfica",
            icon: (
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            ),
        },
        {
            id: "categoria",
            label: "Categoría",
            desc: "Bienes, Servicios y Obras",
            icon: (
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
            ),
        },
        {
            id: "estado",
            label: "Estado Proceso",
            desc: "Adjudicados vs Otros",
            icon: (
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
            ),
        },
    ];

    return (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {options.map((option) => (
                <button
                    key={option.id}
                    onClick={() => onTypeChange(option.id)}
                    className={`flex flex-col items-start rounded-xl border p-4 transition-all ${selectedType === option.id
                            ? "border-indigo-500 bg-indigo-50 dark:border-indigo-400 dark:bg-indigo-900/20"
                            : "border-slate-200/60 bg-white/50 hover:border-indigo-200 hover:bg-white hover:shadow-md dark:border-slate-700/60 dark:bg-slate-800/50 dark:hover:border-slate-600 dark:hover:bg-slate-800"
                        }`}
                >
                    <div
                        className={`mb-3 rounded-lg p-2 ${selectedType === option.id
                                ? "bg-indigo-100 text-indigo-600 dark:bg-indigo-900/50 dark:text-indigo-300"
                                : "bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-400"
                            }`}
                    >
                        {option.icon}
                    </div>
                    <h3 className={`text-sm font-semibold ${selectedType === option.id ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-900 dark:text-white'}`}>
                        {option.label}
                    </h3>
                    <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                        {option.desc}
                    </p>
                </button>
            ))}
        </div>
    );
};
