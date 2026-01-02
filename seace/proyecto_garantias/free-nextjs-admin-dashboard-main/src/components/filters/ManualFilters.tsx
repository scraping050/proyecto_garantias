"use client";
import React, { useState } from "react";

interface ManualFiltersProps {
    onFilterChange: (filters: ManualFilterValues) => void;
    initialFilters?: ManualFilterValues;
}

export interface ManualFilterValues {
    origen?: string;
    estado?: string;
}

export function ManualFilters({ onFilterChange, initialFilters }: ManualFiltersProps) {
    const [origen, setOrigen] = useState(initialFilters?.origen || '');
    const [estado, setEstado] = useState(initialFilters?.estado || 'ACTIVO');

    const handleOrigenChange = (value: string) => {
        setOrigen(value);
        onFilterChange({ origen: value, estado });
    };

    const handleEstadoChange = (value: string) => {
        setEstado(value);
        onFilterChange({ origen, estado: value });
    };

    const handleClear = () => {
        setOrigen('');
        setEstado('ACTIVO');
        onFilterChange({ origen: '', estado: 'ACTIVO' });
    };

    return (
        <div className="rounded-xl border border-gray-200 bg-white px-6 py-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            {/* Header con título y botón limpiar */}
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-base font-semibold text-gray-900 dark:text-white">
                    Filtros de Gestión Manual
                </h3>
                {(origen || estado !== 'ACTIVO') && (
                    <button
                        onClick={handleClear}
                        className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 transition-colors"
                    >
                        Limpiar filtros
                    </button>
                )}
            </div>

            {/* Filtros en línea horizontal */}
            <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
                {/* Filtro por Origen */}
                <div className="flex items-center gap-3">
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
                        <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                        </svg>
                        Origen de Datos
                    </label>
                    <select
                        value={origen}
                        onChange={(e) => handleOrigenChange(e.target.value)}
                        className="min-w-[200px] rounded-lg border-gray-300 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-all"
                    >
                        <option value="">Todas las licitaciones</option>
                        <option value="MANUAL">🟢 Solo Manuales</option>
                        <option value="ETL">🔵 Solo ETL</option>
                        <option value="MODIFICADO">🟡 Solo Modificadas</option>
                    </select>
                </div>

                {/* Filtro por Estado */}
                <div className="flex items-center gap-3">
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">
                        <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Estado del Registro
                    </label>
                    <select
                        value={estado}
                        onChange={(e) => handleEstadoChange(e.target.value)}
                        className="min-w-[160px] rounded-lg border-gray-300 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-all"
                    >
                        <option value="">Todos los estados</option>
                        <option value="ACTIVO">✅ Activas</option>
                        <option value="ELIMINADO">🗑️ Eliminadas</option>
                    </select>
                </div>
            </div>
        </div>
    );
}
