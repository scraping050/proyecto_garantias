"use client";
import React, { useState, useEffect } from "react";
import type { SearchFilters } from "@/types/licitacion";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

interface SearchFiltersProps {
    onFilterChange: (filters: SearchFilters) => void;
    showTitle?: boolean;
    collapsible?: boolean;
    initialFilters?: SearchFilters;
    customTitle?: string;
    customDescription?: string;
    onClear?: () => void;
}

export const SearchFiltersComponent: React.FC<SearchFiltersProps> = ({
    onFilterChange,
    showTitle = true,
    collapsible = false,
    initialFilters,
    customTitle,
    customDescription,
    onClear
}) => {
    const [filters, setFilters] = useState<SearchFilters>(initialFilters || {
        search: "",
        departamento: "",
        provincia: "",
        distrito: "",
        estado_proceso: "",
        categoria: "",
        comprador: "",
        aseguradora: "",
        year: "",
        mes: "",
        tipo_garantia: "",
    });

    const [isExpanded, setIsExpanded] = useState(!collapsible);

    // Estados para opciones dinámicas
    const [departamentos, setDepartamentos] = useState<string[]>([]);
    const [provincias, setProvincias] = useState<string[]>([]);
    const [distritos, setDistritos] = useState<string[]>([]);
    const [estados, setEstados] = useState<string[]>([]);
    const [categorias, setCategorias] = useState<string[]>([]);
    const [compradores, setCompradores] = useState<string[]>([]);
    const [aseguradoras, setAseguradoras] = useState<string[]>([]);
    const [years, setYears] = useState<string[]>([]);
    const [meses, setMeses] = useState<{ value: string, label: string }[]>([]);
    const [tiposGarantia, setTiposGarantia] = useState<string[]>([]);

    // Autocomplete state
    const [suggestions, setSuggestions] = useState<{ texto: string, tipo: string }[]>([]);
    const [showSuggestions, setShowSuggestions] = useState(false);

    // Cargar opciones al montar
    useEffect(() => {
        fetchDepartamentos();
        fetchEstados();
        fetchCategorias();
        fetchCompradores();
        fetchAseguradoras();
        fetchYears();
        fetchMeses();
        fetchTiposGarantia();
    }, []);

    // Cargar provincias cuando cambia departamento
    useEffect(() => {
        if (filters.departamento) {
            fetchProvincias(filters.departamento);
        } else {
            setProvincias([]);
            setDistritos([]);
        }
    }, [filters.departamento]);



    // Fetch suggestions when search changes
    useEffect(() => {
        const fetchSuggestions = async () => {
            if (filters.search && filters.search.length >= 2) {
                try {
                    const response = await fetch(`${API_BASE_URL}/api/licitaciones/suggestions?q=${encodeURIComponent(filters.search)}`);
                    const data = await response.json();
                    setSuggestions(data.data || []);
                    setShowSuggestions(true);
                } catch (error) {
                    console.error("Error fetching suggestions:", error);
                }
            } else {
                setSuggestions([]);
                setShowSuggestions(false);
            }
        };

        const timeoutId = setTimeout(fetchSuggestions, 300); // Debounce 300ms
        return () => clearTimeout(timeoutId);
    }, [filters.search]);

    // Cargar distritos cuando cambia provincia
    useEffect(() => {
        if (filters.provincia) {
            fetchDistritos(filters.provincia);
        } else {
            setDistritos([]);
        }
    }, [filters.provincia]);

    // ... fetch functions ...
    const fetchDepartamentos = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/departamentos`);
            const data = await response.json();
            setDepartamentos(data.data || []);
        } catch (error) {
            console.error("Error fetching departamentos:", error);
        }
    };

    const fetchProvincias = async (departamento: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/provincias?departamento=${encodeURIComponent(departamento)}`);
            const data = await response.json();
            setProvincias(data.data || []);
        } catch (error) {
            console.error("Error fetching provincias:", error);
        }
    };

    const fetchDistritos = async (provincia: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/distritos?provincia=${encodeURIComponent(provincia)}`);
            const data = await response.json();
            setDistritos(data.data || []);
        } catch (error) {
            console.error("Error fetching distritos:", error);
        }
    };

    const fetchEstados = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/estados`);
            const data = await response.json();
            setEstados(data.data || []);
        } catch (error) {
            console.error("Error fetching estados:", error);
        }
    };

    const fetchCategorias = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/categorias`);
            const data = await response.json();
            setCategorias(data.data || []);
        } catch (error) {
            console.error("Error fetching categorias:", error);
        }
    };

    const fetchCompradores = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/compradores`);
            const data = await response.json();
            setCompradores(data.data || []);
        } catch (error) {
            console.error("Error fetching compradores:", error);
        }
    };

    const fetchAseguradoras = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/aseguradoras`);
            const data = await response.json();
            setAseguradoras(data.data || []);
        } catch (error) {
            console.error("Error fetching aseguradoras:", error);
        }
    };

    const fetchYears = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/years`);
            const data = await response.json();
            setYears(data.data || []);
        } catch (error) {
            console.error("Error fetching years:", error);
        }
    };

    const fetchMeses = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/meses`);
            const data = await response.json();
            setMeses(data.data || []);
        } catch (error) {
            console.error("Error fetching meses:", error);
        }
    };

    const fetchTiposGarantia = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/filtros/tipos-garantia`);
            const data = await response.json();
            // Filtrar explícitamente POLIZA por si el backend está en caché o pendiente de reinicio
            const filteredData = (data.data || []).filter((t: string) => t && !t.toUpperCase().includes('POLIZA'));
            setTiposGarantia(filteredData);
        } catch (error) {
            console.error("Error fetching tipos garantia:", error);
        }
    };


    const handleFilterChange = (key: keyof SearchFilters, value: any) => {
        const newFilters = { ...filters, [key]: value };

        // Si cambia departamento, resetear provincia y distrito
        if (key === "departamento") {
            newFilters.provincia = "";
            newFilters.distrito = "";
        }

        // Si cambia provincia, resetear distrito
        if (key === "provincia") {
            newFilters.distrito = "";
        }

        setFilters(newFilters);
        onFilterChange(newFilters);
    };

    const handleReset = () => {
        const resetFilters: SearchFilters = {
            search: "",
            departamento: "",
            provincia: "",
            distrito: "",
            estado_proceso: "",
            categoria: "",
            comprador: "",
            aseguradora: "",
            year: "",
            mes: "",
        };
        setFilters(resetFilters);
        onFilterChange(resetFilters);
        if (onClear) onClear();
    };

    // Highlight Effect State
    const [isHighlighting, setIsHighlighting] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsHighlighting(false);
        }, 7000);
        return () => clearTimeout(timer);
    }, []);

    const activeFiltersCount = Object.values(filters).filter(v => v !== "" && v !== null).length;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                {showTitle ? (
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                            {customTitle || "Búsqueda Avanzada de Licitaciones"}
                        </h2>
                        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                            {customDescription || "Filtra y encuentra licitaciones de manera rápida y precisa"}
                        </p>
                    </div>
                ) : (
                    <div />
                )}

                <div className="flex gap-3 w-full sm:w-auto">
                    {collapsible && (
                        <button
                            onClick={() => setIsExpanded(!isExpanded)}
                            className={`relative flex items-center gap-2 px-5 py-2.5 text-sm font-bold text-white rounded-xl transition-all shadow-md hover:shadow-lg ${isExpanded
                                ? 'bg-indigo-700 ring-2 ring-indigo-300'
                                : 'bg-indigo-600 hover:bg-indigo-500'
                                }`}
                        >
                            {isHighlighting && (
                                <span className="absolute inset-0 inline-flex h-full w-full rounded-xl bg-indigo-500 opacity-60 animate-ping"></span>
                            )}

                            <span className="relative z-10">{isExpanded ? 'Menos Filtros' : 'Más Filtros'}</span>
                            <svg className={`relative z-10 w-5 h-5 transition-transform ${isExpanded ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>
                    )}

                    <button
                        onClick={handleReset}
                        className="relative flex items-center gap-2 px-5 py-2.5 text-sm font-bold text-red-600 bg-red-50 border-2 border-red-100 rounded-xl hover:bg-red-100 hover:border-red-200 transition-all shadow-sm hover:shadow-md"
                        title="Limpiar todos los filtros"
                    >
                        {isHighlighting && (
                            <span className="absolute inset-0 inline-flex h-full w-full rounded-xl bg-red-400 opacity-50 animate-ping"></span>
                        )}
                        <svg className="relative z-10 w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        <span className="relative z-10">Limpiar</span>
                    </button>
                </div>
            </div>

            {/* Search Bar & Primary Filters */}
            <div className="space-y-4">
                {/* Search Bar */}
                {/* Search Bar with Autocomplete */}
                <div className="relative">
                    <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4 z-10">
                        <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                    <input
                        type="text"
                        value={filters.search}
                        onChange={(e) => {
                            handleFilterChange("search", e.target.value);
                            // Fetch suggestions logic is handled by a separate effect below
                        }}
                        onFocus={() => filters.search.length >= 2 && setShowSuggestions(true)}
                        onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                        placeholder="Buscar por descripción, comprador, nomenclatura, ganador, banco..."
                        className="block w-full rounded-xl border border-gray-300 bg-white py-2.5 pl-12 pr-4 text-gray-900 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder-gray-500"
                        autoComplete="off"
                    />

                    {/* Suggestions Dropdown */}
                    {showSuggestions && suggestions.length > 0 && (
                        <div className="absolute z-50 mt-1 w-full rounded-xl border border-gray-200 bg-white py-1 shadow-lg dark:border-gray-700 dark:bg-gray-800">
                            {suggestions.map((item, index) => (
                                <button
                                    key={index}
                                    onClick={() => {
                                        handleFilterChange("search", item.texto);
                                        setShowSuggestions(false);
                                    }}
                                    className="flex w-full items-center justify-between px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-700"
                                >
                                    <span className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                        {item.texto}
                                    </span>
                                    <span className="ml-2 flex-shrink-0 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-500 dark:bg-gray-900 dark:text-gray-400">
                                        {item.tipo}
                                    </span>
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* Primary Filters (Always Visible) */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    {/* Departamento */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Departamento
                        </label>
                        <select
                            value={filters.departamento}
                            onChange={(e) => handleFilterChange("departamento", e.target.value)}
                            className="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                        >
                            <option value="">Todos los departamentos</option>
                            {departamentos.map((dept) => (
                                <option key={dept} value={dept}>{dept}</option>
                            ))}
                        </select>
                    </div>

                    {/* Estado del Proceso */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Estado del Proceso
                        </label>
                        <select
                            value={filters.estado_proceso}
                            onChange={(e) => handleFilterChange("estado_proceso", e.target.value)}
                            className="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                        >
                            <option value="">Todos los estados</option>
                            {estados.map((estado) => (
                                <option key={estado} value={estado}>{estado}</option>
                            ))}
                        </select>
                    </div>

                    {/* Categoría */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Categoría
                        </label>
                        <select
                            value={filters.categoria}
                            onChange={(e) => handleFilterChange("categoria", e.target.value)}
                            className="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                        >
                            <option value="">Todas las categorías</option>
                            {categorias.map((cat) => (
                                <option key={cat} value={cat}>{cat}</option>
                            ))}
                        </select>
                    </div>

                    {/* Año */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Periodo
                        </label>
                        <div className="flex gap-2">
                            <select
                                value={filters.year}
                                onChange={(e) => handleFilterChange("year", e.target.value)}
                                className="block w-1/2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            >
                                <option value="">Año</option>
                                {years.map((year) => (
                                    <option key={year} value={year}>{year}</option>
                                ))}
                            </select>
                            <select
                                value={filters.mes}
                                onChange={(e) => handleFilterChange("mes", e.target.value)}
                                className="block w-1/2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            >
                                <option value="">Mes</option>
                                {Array.isArray(meses) && meses.map((mes) => (
                                    <option key={mes.value} value={mes.value}>{mes.label}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            {/* Advanced Filters (Collapsible) */}
            {isExpanded && (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 animate-fade-in-down">
                    {/* Ubicacion Detallada (Provincia + Distrito) - Grouped */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Ubicación Detallada
                        </label>
                        <div className="flex gap-2">
                            <select
                                value={filters.provincia}
                                onChange={(e) => handleFilterChange("provincia", e.target.value)}
                                disabled={!filters.departamento}
                                className="block w-1/2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            >
                                <option value="">Provincia</option>
                                {provincias.map((prov) => (
                                    <option key={prov} value={prov}>{prov}</option>
                                ))}
                            </select>
                            <select
                                value={filters.distrito}
                                onChange={(e) => handleFilterChange("distrito", e.target.value)}
                                disabled={!filters.provincia}
                                className="block w-1/2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            >
                                <option value="">Distrito</option>
                                {distritos.map((dist) => (
                                    <option key={dist} value={dist}>{dist}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Tipo de Garantía - New Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Tipo de Garantía
                        </label>
                        <select
                            value={filters.tipo_garantia || ""}
                            onChange={(e) => handleFilterChange("tipo_garantia", e.target.value)}
                            className="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                        >
                            <option value="">Todos los tipos</option>
                            {tiposGarantia.map((tipo) => (
                                <option key={tipo} value={tipo}>{tipo}</option>
                            ))}
                        </select>
                    </div>

                    {/* Aseguradora */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Aseguradora
                        </label>
                        <select
                            value={filters.aseguradora}
                            onChange={(e) => handleFilterChange("aseguradora", e.target.value)}
                            className="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                        >
                            <option value="">Todas las aseguradoras</option>
                            {aseguradoras.map((aseg) => (
                                <option key={aseg} value={aseg}>{aseg}</option>
                            ))}
                        </select>
                    </div>

                    {/* Entidad o Consorcio */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Entidad o Consorcio
                        </label>
                        <select
                            value={filters.comprador}
                            onChange={(e) => handleFilterChange("comprador", e.target.value)}
                            className="block w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                        >
                            <option value="">Todas las entidades</option>
                            {compradores.slice(0, 100).map((comp) => (
                                <option key={comp} value={comp}>{comp}</option>
                            ))}
                        </select>
                    </div>


                </div>
            )}

            {/* Active Filters Count */}
            {activeFiltersCount > 0 && (
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                    </svg>
                    <span className="font-medium">
                        {activeFiltersCount} filtro(s) activo(s)
                    </span>
                </div>
            )}
        </div>
    );
};
