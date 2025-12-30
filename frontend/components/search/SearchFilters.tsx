"use client";

import React, { useEffect, useState } from "react";
import type { SearchFilters } from "@/types/licitacion";
import { Search, X, Filter } from "lucide-react";

interface Props {
    onFilterChange: (filters: SearchFilters) => void;
    initialFilters?: SearchFilters;
}

interface FilterOptions {
    estados: string[];
    aseguradoras: string[];
    tipos_entidad: string[];
    objetos: string[];
    departamentos: string[];
}

export const SearchFiltersComponent: React.FC<Props> = ({
    onFilterChange,
    initialFilters = {},
}) => {
    // Default Options
    const DEFAULT_DEPARTAMENTOS = [
        "AMAZONAS", "ANCASH", "APURIMAC", "AREQUIPA", "AYACUCHO", "CAJAMARCA", "CALLAO",
        "CUSCO", "HUANCAVELICA", "HUANUCO", "ICA", "JUNIN", "LA LIBERTAD", "LAMBAYEQUE",
        "LIMA", "LORETO", "MADRE DE DIOS", "MOQUEGUA", "PASCO", "PIURA", "PUNO",
        "SAN MARTIN", "TACNA", "TUMBES", "UCAYALI"
    ];

    const DEFAULT_ESTADOS = ["CONVOCADO", "ADJUDICADO", "DESIERTO", "CANCELADO", "SUSPENDIDO"];
    const DEFAULT_CATEGORIAS = ["BIENES", "SERVICIOS", "OBRAS", "CONSULTORIA DE OBRAS"];
    const DEFAULT_ASEGURADORAS = ["SECREX", "AVLA", "INSUR", "MAPFRE", "CRECER", "LIBERTY", "MUNDIAL"];

    const [localFilters, setLocalFilters] = useState<SearchFilters>(initialFilters);
    const [options, setOptions] = useState<FilterOptions>({
        estados: DEFAULT_ESTADOS,
        aseguradoras: DEFAULT_ASEGURADORAS,
        tipos_entidad: [],
        objetos: DEFAULT_CATEGORIAS,
        departamentos: DEFAULT_DEPARTAMENTOS
    });

    useEffect(() => {
        const fetchOptions = async () => {
            try {
                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/dashboard/filter-options`);
                if (res.ok) {
                    const data = await res.json();

                    // Only update if we get valid data, otherwise keep defaults or merge distinct
                    setOptions(prev => ({
                        estados: data.estados?.length ? data.estados : prev.estados,
                        aseguradoras: data.aseguradoras?.length ? data.aseguradoras : prev.aseguradoras,
                        tipos_entidad: data.tipos_entidad || [],
                        objetos: data.objetos?.length ? data.objetos : prev.objetos,
                        departamentos: data.departamentos?.length ? data.departamentos : prev.departamentos
                    }));
                }
            } catch (error) {
                console.error("Error fetching filter options, using defaults:", error);
            }
        };
        fetchOptions();
    }, []);

    const handleChange = (key: keyof SearchFilters, value: string) => {
        setLocalFilters(prev => ({ ...prev, [key]: value }));
    };

    const handleApply = () => {
        onFilterChange(localFilters);
    };

    const handleClear = () => {
        const emptyFilters = {};
        setLocalFilters(emptyFilters);
        onFilterChange(emptyFilters);
    };

    const inputClasses =
        "w-full rounded-xl border border-slate-200/80 bg-slate-50/50 px-4 py-2.5 text-sm text-slate-700 placeholder-slate-400 shadow-sm transition-all focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 dark:border-white/10 dark:bg-[#0b122b] dark:text-slate-200 dark:placeholder-slate-500/50";

    const labelClasses =
        "mb-1.5 block text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400";

    return (
        <div className="space-y-6">

            {/* Header with Title and Buttons */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-100 dark:border-white/5">
                <div className="flex items-start gap-3">
                    <div className="p-2.5 rounded-xl bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400">
                        <Search className="w-5 h-5" />
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                            Búsqueda Avanzada de Licitaciones
                        </h3>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                            Filtra y encuentra licitaciones de manera rápida y precisa
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={handleClear}
                        className="group flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-200 bg-white text-xs font-bold text-slate-600 hover:bg-slate-50 hover:text-slate-800 hover:border-slate-300 transition-all dark:bg-[#0b122b] dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                    >
                        <X className="w-3.5 h-3.5 group-hover:rotate-180 transition-transform duration-500" />
                        <span className="sr-only sm:not-sr-only">Limpiar</span>
                    </button>
                    <button
                        onClick={handleApply}
                        className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-white text-xs font-bold hover:bg-blue-700 shadow-md shadow-blue-500/20 transition-all"
                    >
                        <Filter className="w-3.5 h-3.5" />
                        <span>Aplicar Filtros</span>
                    </button>
                </div>
            </div>

            {/* Inputs Grid */}
            <div className="space-y-6">

                {/* Search Bar */}
                <div>
                    <div className="relative group">
                        <input
                            type="text"
                            placeholder="Buscar por descripción, comprador, nomenclatura..."
                            className={`${inputClasses} pl-11 py-3 bg-white border-slate-200 shadow-sm group-focus-within:shadow-md transition-shadow`}
                            value={localFilters.search || ""}
                            onChange={(e) => handleChange("search", e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleApply()}
                        />
                        <Search className="absolute left-4 top-3.5 h-4 w-4 text-slate-400 group-focus-within:text-blue-500 transition-colors" />
                    </div>
                </div>

                {/* Filters Row 1 */}
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

                    {/* Departamento */}
                    <div>
                        <label className={labelClasses}>Departamento</label>
                        <select
                            className={inputClasses}
                            value={localFilters.departamento || ""}
                            onChange={(e) => handleChange("departamento", e.target.value)}
                        >
                            <option value="">Todos los departamentos</option>
                            {options.departamentos.map((dept) => (
                                <option key={dept} value={dept}>{dept}</option>
                            ))}
                        </select>
                    </div>

                    {/* Provincia */}
                    <div>
                        <label className={labelClasses}>Provincia</label>
                        <input
                            type="text"
                            placeholder="Todas las provincias"
                            className={inputClasses}
                            value={localFilters.provincia || ""}
                            onChange={(e) => handleChange("provincia", e.target.value)}
                        />
                    </div>

                    {/* Distrito */}
                    <div>
                        <label className={labelClasses}>Distrito</label>
                        <input
                            type="text"
                            placeholder="Todos los distritos"
                            className={inputClasses}
                            value={localFilters.distrito || ""}
                            onChange={(e) => handleChange("distrito", e.target.value)}
                        />
                    </div>

                    {/* Estado */}
                    <div>
                        <label className={labelClasses}>Estado del Proceso</label>
                        <select
                            className={inputClasses}
                            value={localFilters.estado_proceso || ""}
                            onChange={(e) => handleChange("estado_proceso", e.target.value)}
                        >
                            <option value="">Todos los estados</option>
                            {options.estados.map((est) => (
                                <option key={est} value={est}>{est}</option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* Filters Row 2 */}
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

                    {/* Categoría */}
                    <div>
                        <label className={labelClasses}>Categoría</label>
                        <select
                            className={inputClasses}
                            value={localFilters.categoria || ""}
                            onChange={(e) => handleChange("categoria", e.target.value)}
                        >
                            <option value="">Todas las categorías</option>
                            {options.objetos.map((cat) => (
                                <option key={cat} value={cat}>{cat}</option>
                            ))}
                        </select>
                    </div>

                    {/* Entidad (Comprador) */}
                    <div>
                        <label className={labelClasses}>Entidad o Consorcio</label>
                        <input
                            type="text"
                            placeholder="Todas las entidades"
                            className={inputClasses}
                            value={localFilters.comprador || ""}
                            onChange={(e) => handleChange("comprador", e.target.value)}
                        />
                    </div>

                    {/* Aseguradora */}
                    <div>
                        <label className={labelClasses}>Aseguradora</label>
                        <select
                            className={inputClasses}
                            value={localFilters.aseguradora || ""}
                            onChange={(e) => handleChange("aseguradora", e.target.value)}
                        >
                            <option value="">Todas las aseguradoras</option>
                            {options.aseguradoras.map((seg) => (
                                <option key={seg} value={seg}>{seg}</option>
                            ))}
                        </select>
                    </div>

                    {/* Año */}
                    <div>
                        <label className={labelClasses}>Año</label>
                        <select
                            className={inputClasses}
                            value={localFilters.year || ""}
                            onChange={(e) => handleChange("year", e.target.value)}
                        >
                            <option value="">Todos los años</option>
                            {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i + 1).map(y => (
                                <option key={y} value={y}>{y}</option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* Advanced Row (Collapsible usually, but open here per design, minimal month) */}
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-4">
                    <div>
                        <label className={labelClasses}>Mes</label>
                        <select
                            className={inputClasses}
                            value={localFilters.mes || ""}
                            onChange={(e) => handleChange("mes", e.target.value)}
                        >
                            <option value="">Todos los meses</option>
                            {["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"].map((m, i) => (
                                <option key={i} value={i + 1}>{m}</option>
                            ))}
                        </select>
                    </div>
                </div>

            </div>
        </div>
    );
};
