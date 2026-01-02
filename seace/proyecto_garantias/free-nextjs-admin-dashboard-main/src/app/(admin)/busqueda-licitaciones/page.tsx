"use client";
import React, { useState, useEffect, useCallback } from "react";
import type { Metadata } from "next";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { SearchFiltersComponent } from "@/components/search/SearchFilters";
import { LicitacionCard } from "@/components/search/LicitacionCard";
import type { Licitacion, SearchFilters } from "@/types/licitacion";

// Helper hook since we are not using a shared lib
function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState(value);
    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);
        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);
    return debouncedValue;
}

// Extract logic to inner component
function BusquedaContent() {
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();

    // Initialize state from URL Params
    const initialFilters: SearchFilters = {
        search: searchParams.get('search') || "",
        departamento: searchParams.get('departamento') || "",
        provincia: searchParams.get('provincia') || "",
        distrito: searchParams.get('distrito') || "",
        estado_proceso: searchParams.get('estado_proceso') || "",
        categoria: searchParams.get('categoria') || "",
        comprador: searchParams.get('comprador') || "",
        aseguradora: searchParams.get('entidad_financiera') || "",
        year: searchParams.get('year') || "",
        mes: searchParams.get('mes') || "",
    };

    const initialPage = Number(searchParams.get('page')) || 1;
    const initialSort = searchParams.get('sort') || 'fecha_desc';

    const [licitaciones, setLicitaciones] = useState<Licitacion[]>([]);
    // const [filteredLicitaciones, setFilteredLicitaciones] = useState<Licitacion[]>([]); // Removed
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(initialPage);
    const [sortBy, setSortBy] = useState<string>(initialSort);
    const [itemsPerPage, setItemsPerPage] = useState(12);
    const [filters, setFilters] = useState<SearchFilters>(initialFilters);
    const [totalRecords, setTotalRecords] = useState(0);

    // Update URL helper
    const updateURL = useCallback((newFilters: SearchFilters, page: number, sort: string) => {
        const params = new URLSearchParams();
        if (newFilters.search) params.set('search', newFilters.search);
        if (newFilters.departamento) params.set('departamento', newFilters.departamento);
        if (newFilters.provincia) params.set('provincia', newFilters.provincia);
        if (newFilters.distrito) params.set('distrito', newFilters.distrito);
        if (newFilters.estado_proceso) params.set('estado_proceso', newFilters.estado_proceso);
        if (newFilters.categoria) params.set('categoria', newFilters.categoria);
        if (newFilters.comprador) params.set('comprador', newFilters.comprador);
        if (newFilters.aseguradora) params.set('entidad_financiera', newFilters.aseguradora);
        if (newFilters.year) params.set('year', newFilters.year);
        if (newFilters.mes) params.set('mes', newFilters.mes);

        params.set('page', page.toString());
        params.set('sort', sort);

        router.replace(`${pathname}?${params.toString()}`);
    }, [pathname, router]);

    // Debounce filters
    const debouncedFilters = useDebounce(filters, 600);

    // Fetch data from API with filters
    const fetchLicitaciones = async (currentFilters: SearchFilters, page: number, perPage: number, sort: string) => {
        try {
            setLoading(true);

            // Construir query params for API
            const queryParams = new URLSearchParams();

            if (currentFilters.search) queryParams.append('search', currentFilters.search);
            if (currentFilters.departamento) queryParams.append('departamento', currentFilters.departamento);
            if (currentFilters.provincia) queryParams.append('provincia', currentFilters.provincia);
            if (currentFilters.distrito) queryParams.append('distrito', currentFilters.distrito);
            if (currentFilters.estado_proceso) queryParams.append('estado_proceso', currentFilters.estado_proceso);
            if (currentFilters.categoria) queryParams.append('categoria', currentFilters.categoria);
            if (currentFilters.comprador) queryParams.append('comprador', currentFilters.comprador);
            if (currentFilters.aseguradora) queryParams.append('entidad_financiera', currentFilters.aseguradora);
            if (currentFilters.year) queryParams.append('year', currentFilters.year);
            if (currentFilters.mes) queryParams.append('mes', currentFilters.mes);

            // Agregar paginación y ordenamiento
            queryParams.append('page', page.toString());
            queryParams.append('per_page', perPage.toString());
            queryParams.append('sort', sort);

            const url = `http://localhost:5000/api/licitaciones?${queryParams}`;
            const response = await fetch(url);
            const data = await response.json();

            // Deduplicate items by id_convocatoria to prevent React key errors
            const uniqueItems = Array.from(
                new Map((data.data || []).map((item: Licitacion) => [item.id_convocatoria, item])).values()
            ) as Licitacion[];

            setLicitaciones(uniqueItems);
            setTotalRecords(data.pagination?.total || uniqueItems.length);
        } catch (error) {
            console.error("Error fetching licitaciones:", error);
            setLicitaciones([]);
            setTotalRecords(0);
        } finally {
            setLoading(false);
        }
    };

    // Auto-Fetch when debounced filters, page, itemsPerPage, or sort changes
    useEffect(() => {
        fetchLicitaciones(debouncedFilters, currentPage, itemsPerPage, sortBy);
        // Also update URL to keep state shareable
        updateURL(debouncedFilters, currentPage, sortBy);
    }, [debouncedFilters, currentPage, itemsPerPage, sortBy, updateURL]);

    // Handle filter changes - JUST update state, debouncer handles fetch
    const handleFilterChange = (newFilters: SearchFilters) => {
        setFilters(newFilters);
        setCurrentPage(1); // Always reset to page 1 on filter change
    };

    // Handle sort change
    const handleSortChange = (newSort: string) => {
        setSortBy(newSort);
        // fetch triggered by useEffect on sortBy change
        updateURL(filters, currentPage, newSort);
    };

    // Pagination
    const totalPages = Math.ceil(totalRecords / itemsPerPage);

    // Generate page numbers with ellipsis
    const getPageNumbers = () => {
        const pages: (number | string)[] = [];
        const maxVisible = 5; // Maximum number of page buttons to show

        if (totalPages <= maxVisible + 2) {
            // Show all pages if total is small
            for (let i = 1; i <= totalPages; i++) {
                pages.push(i);
            }
        } else {
            // Always show first page
            pages.push(1);

            if (currentPage > 3) {
                pages.push('...');
            }

            // Show pages around current page
            const start = Math.max(2, currentPage - 1);
            const end = Math.min(totalPages - 1, currentPage + 1);

            for (let i = start; i <= end; i++) {
                pages.push(i);
            }

            if (currentPage < totalPages - 2) {
                pages.push('...');
            }

            // Always show last page
            if (totalPages > 1) {
                pages.push(totalPages);
            }
        }

        return pages;
    };

    return (
        <div className="space-y-6">
            {/* Filters */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
                <SearchFiltersComponent onFilterChange={handleFilterChange} initialFilters={filters} collapsible={true} />
            </div>

            {/* Results Header */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Resultados de Búsqueda
                    </h3>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        {totalRecords} licitación(es) encontrada(s)
                    </p>
                </div>
                <div className="flex items-center gap-4">
                    {/* Sort Selector */}
                    <div className="flex items-center gap-2">
                        <label htmlFor="sort" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            Ordenar por:
                        </label>
                        <select
                            id="sort"
                            value={sortBy}
                            onChange={(e) => handleSortChange(e.target.value)}
                            className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                        >
                            <option value="fecha_desc">Fecha (más reciente)</option>
                            <option value="fecha_asc">Fecha (más antigua)</option>
                            <option value="monto_desc">Monto (mayor)</option>
                            <option value="monto_asc">Monto (menor)</option>
                            <option value="nombre_asc">Nombre (A-Z)</option>
                            <option value="nombre_desc">Nombre (Z-A)</option>
                        </select>
                    </div>
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                        Página {currentPage} de {totalPages || 1}
                    </span>
                </div>
            </div>

            {/* Loading State */}
            {loading && (
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {[...Array(6)].map((_, i) => (
                        <div
                            key={i}
                            className="h-96 animate-pulse rounded-xl bg-gray-200 dark:bg-gray-800"
                        ></div>
                    ))}
                </div>
            )}

            {/* Empty State */}
            {!loading && licitaciones.length === 0 && (
                <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-300 bg-white p-12 dark:border-gray-700 dark:bg-gray-900">
                    <svg
                        className="h-16 w-16 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                    </svg>
                    <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                        No se encontraron resultados
                    </h3>
                    <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                        Intenta ajustar los filtros de búsqueda
                    </p>
                </div>
            )}

            {/* Results Grid */}
            {!loading && licitaciones.length > 0 && (
                <>
                    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                        {licitaciones.map((licitacion) => (
                            <LicitacionCard key={licitacion.id_convocatoria} licitacion={licitacion} showDownload={false} />
                        ))}
                    </div>

                    {/* Pagination */}
                    {totalPages > 1 && (
                        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mt-6">
                            {/* Items per page selector */}
                            <div className="flex items-center gap-2">
                                <label htmlFor="perPage" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Mostrar:
                                </label>
                                <select
                                    id="perPage"
                                    value={itemsPerPage}
                                    onChange={(e) => {
                                        setItemsPerPage(Number(e.target.value));
                                        setCurrentPage(1);
                                    }}
                                    className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                                >
                                    <option value="12">12</option>
                                    <option value="24">24</option>
                                    <option value="48">48</option>
                                    <option value="96">96</option>
                                </select>
                                <span className="text-sm text-gray-500 dark:text-gray-400">por página</span>
                            </div>

                            {/* Page navigation */}
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                                    disabled={currentPage === 1}
                                    className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                                >
                                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                                    </svg>
                                    Anterior
                                </button>

                                <div className="flex items-center gap-1">
                                    {getPageNumbers().map((page, index) => (
                                        page === '...' ? (
                                            <span key={`ellipsis-${index}`} className="px-2 text-gray-500 dark:text-gray-400">
                                                ...
                                            </span>
                                        ) : (
                                            <button
                                                key={page}
                                                onClick={() => setCurrentPage(page as number)}
                                                className={`h-10 w-10 rounded-lg text-sm font-semibold transition-colors ${currentPage === page
                                                    ? "bg-indigo-600 text-white"
                                                    : "bg-white text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                                                    }`}
                                            >
                                                {page}
                                            </button>
                                        )
                                    ))}
                                </div>

                                <button
                                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                                    disabled={currentPage === totalPages}
                                    className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                                >
                                    Siguiente
                                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

export default function BusquedaLicitaciones() {
    return (
        <React.Suspense fallback={<div className="flex h-screen items-center justify-center">Cargando buscador...</div>}>
            <BusquedaContent />
        </React.Suspense>
    );
}
