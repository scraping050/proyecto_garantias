"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import type { ReportType, SearchFilters, Licitacion } from "@/types/licitacion";
import { SearchFiltersComponent } from "@/components/search/SearchFilters";
import { LicitacionCard } from "@/components/search/LicitacionCard";
import { AddLicitacionButton } from "@/components/gestion-manual/AddLicitacionButton";
import { LicitacionFormModal } from "@/components/gestion-manual/LicitacionFormModal";
import { DeleteConfirmationModal } from "@/components/gestion-manual/DeleteConfirmationModal";
import { exportToPDF, exportToExcel, exportToCSV } from "@/lib/exportUtils";

// Helper Hook
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

function GestionManualContent() {
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();

    // Initialize state from URL params
    const initialType = (searchParams.get("type") as ReportType) || "personalizado";
    const initialFilters: SearchFilters = {
        search: searchParams.get("search") || "",
        departamento: searchParams.get("departamento") || "",
        provincia: searchParams.get("provincia") || "",
        distrito: searchParams.get("distrito") || "",
        estado_proceso: searchParams.get("estado_proceso") || "",
        categoria: searchParams.get("categoria") || "",
        comprador: searchParams.get("comprador") || "",
        aseguradora: searchParams.get("entidad_financiera") || "",
        year: searchParams.get("year") || "",
        mes: searchParams.get("mes") || "",
    };

    const [selectedType, setSelectedType] = useState<ReportType>(initialType);
    const [filters, setFilters] = useState<SearchFilters>(initialFilters);
    const [reportData, setReportData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [exporting, setExporting] = useState(false);
    const [hasInitialFetch, setHasInitialFetch] = useState(false);
    const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
    const [error, setError] = useState<string | null>(null); // Added error state

    // Pagination State
    const [currentPage, setCurrentPage] = useState(1);
    const [paginationData, setPaginationData] = useState({ total: 0, totalPages: 1, limit: 20, page: 1 });

    // Debounce
    const debouncedFilters = useDebounce(filters, 600);

    // CRUD Modal States
    const [isFormModalOpen, setIsFormModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [formMode, setFormMode] = useState<"create" | "edit">("create");
    const [selectedLicitacion, setSelectedLicitacion] = useState<Licitacion | null>(null);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [highlightId, setHighlightId] = useState<string | null>(null);

    // Manual filters state - simplified to just origen_tipo
    const [origenTipo, setOrigenTipo] = useState<string>('');

    // Columns config for "personalizado" type
    const allPersonalizedColumns = [
        { key: "id_convocatoria", label: "ID Convocatoria" },
        { key: "descripcion", label: "Descripción" },
        { key: "monto_estimado", label: "Monto Estimado" },
        { key: "entidad", label: "Entidad/Comprador" },
        { key: "departamento", label: "Departamento" },
        { key: "estado_proceso", label: "Estado" },
        { key: "fecha_publicacion", label: "Fecha Pub." },
        { key: "tipo_garantia", label: "Tipo Garantía" },
        { key: "monto_adjudicado", label: "Monto Adj." },
        { key: "entidad_financiera", label: "Entidad Financiera" },
    ];

    const [visibleColumns, setVisibleColumns] = useState<string[]>([
        "descripcion", "monto_estimado", "entidad", "departamento", "estado_proceso"
    ]);
    const [isOriginDropdownOpen, setIsOriginDropdownOpen] = useState(false);

    const originOptions = [
        { id: '', label: 'Todos', icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' },
        { id: 'MANUAL', label: 'Manuales', icon: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' },
        { id: 'ETL', label: 'Automático', icon: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' },
    ];

    // Update URL when filters or type change
    const updateURL = (newFilters: SearchFilters, type: ReportType) => {
        const params = new URLSearchParams();
        params.set("type", type);

        if (newFilters.search) params.set("search", newFilters.search);
        if (newFilters.departamento) params.set("departamento", newFilters.departamento);
        if (newFilters.provincia) params.set("provincia", newFilters.provincia);
        if (newFilters.distrito) params.set("distrito", newFilters.distrito);
        if (newFilters.estado_proceso) params.set("estado_proceso", newFilters.estado_proceso);
        if (newFilters.categoria) params.set("categoria", newFilters.categoria);
        if (newFilters.comprador) params.set("comprador", newFilters.comprador);
        if (newFilters.aseguradora) params.set("entidad_financiera", newFilters.aseguradora);
        if (newFilters.year) params.set("year", newFilters.year);
        if (newFilters.mes) params.set("mes", newFilters.mes);

        router.replace(`${pathname}?${params.toString()}`);
    };

    const handleFilterChange = (newFilters: SearchFilters) => {
        setFilters(newFilters);
    };

    const handleGenerateReport = async () => {
        setSelectedIds(new Set());
        setCurrentPage(1); // Reset to page 1 on new filter generation
        updateURL(filters, selectedType);
        fetchReport(filters, selectedType, undefined, 1);
    };

    // Auto-search effect
    useEffect(() => {
        // Only trigger if we have valid filters and not initial empty mount (optional)
        handleGenerateReport();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [debouncedFilters]);

    // Clear highlight after 3 seconds
    useEffect(() => {
        if (highlightId) {
            // Scroll to element
            setTimeout(() => {
                const el = document.getElementById(`licitacion-${highlightId}`);
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);

            const timer = setTimeout(() => {
                setHighlightId(null);
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [highlightId]);

    const fetchReport = async (currentFilters: SearchFilters, currentType: ReportType, queryOrigen?: string, pageOverride?: number) => {
        setLoading(true);
        setError(null);
        const page = pageOverride || currentPage;

        try {
            const response = await fetch('/api/reportes/generar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tipo: currentType,
                    page: page,
                    limit: 20,
                    filtros: {
                        ...currentFilters,
                        origen_tipo: queryOrigen !== undefined ? queryOrigen : origenTipo
                    }
                })
            });

            const result = await response.json();

            if (result.success) {
                // Update Pagination Data if verified
                if (result.pagination) {
                    setPaginationData(result.pagination);
                    setCurrentPage(result.pagination.page);
                } else {
                    // Fallback for non-paginated endpoints
                    setPaginationData({ total: Array.isArray(result.data) ? result.data.length : 0, totalPages: 1, limit: 20, page: 1 });
                }

                const dataArray = Array.isArray(result.data) ? result.data : []; // Handle non-array data robustly

                const uniqueItems = Array.from(
                    new Map(dataArray.map((item: any) => [item.id_convocatoria, item])).values()
                );
                setReportData(uniqueItems);
                // Don't auto-select everything on page load, it's confusing with pagination. 
                // retained explicit selection logic if user wants it, but usually bad UX for paginated data.
                // setSelectedIds(new Set(uniqueItems.map((item: any) => item.id_convocatoria))); 
            } else {
                console.error("Error en respuesta:", result.error);
                setError("Error al generar el reporte: " + result.error);
                alert("Error al generar el reporte");
            }
        } catch (error) {
            console.error("Error generando reporte:", error);
            setError("Error al conectar con el servidor");
            alert("Error al conectar con el servidor");
        } finally {
            setLoading(false);
        }
    };

    // ... fetchReport code ...

    const handlePageChange = (newPage: number) => {
        if (newPage < 1 || newPage > paginationData.totalPages) return;
        setCurrentPage(newPage);
        fetchReport(filters, selectedType, undefined, newPage);
        // Scroll to top of list
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Auto-fetch if there are params on mount
    useEffect(() => {
        const hasParams = Array.from(searchParams.keys()).length > 0;
        if (hasParams && !hasInitialFetch) {
            fetchReport(filters, selectedType);
            setHasInitialFetch(true);
        }
    }, [searchParams]);

    // ==================== CRUD HANDLERS ====================

    const handleCreate = () => {
        setFormMode("create");
        setSelectedLicitacion(null);
        setIsFormModalOpen(true);
    };

    const handleEdit = (licitacion: Licitacion) => {
        setFormMode("edit");
        setSelectedLicitacion(licitacion);
        setIsFormModalOpen(true);
    };

    const handleDelete = (licitacion: Licitacion) => {
        setSelectedLicitacion(licitacion);
        setIsDeleteModalOpen(true);
    };

    const handleDuplicate = async (licitacion: Licitacion) => {
        try {
            const response = await fetch(`/api/licitaciones/${licitacion.id_convocatoria}/duplicar`, {
                method: 'POST',
            });

            const result = await response.json();

            if (result.success) {
                alert("Licitación duplicada exitosamente");
                // Refresh data
                fetchReport(filters, selectedType);
            } else {
                alert("Error al duplicar: " + result.error);
            }
        } catch (error) {
            console.error("Error duplicating:", error);
            alert("Error al duplicar la licitación");
        }
    };

    const handleSave = async (data: Partial<Licitacion>) => {
        setIsSaving(true);
        try {
            const url = formMode === "create"
                ? '/api/licitaciones/crear'
                : `/api/licitaciones/${selectedLicitacion?.id_convocatoria}/editar`;

            const method = formMode === "create" ? 'POST' : 'PUT';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                alert(formMode === "create" ? "Licitación creada exitosamente" : "Licitación actualizada exitosamente");
                setIsFormModalOpen(false);
                // Refresh data
                // Ensure we use the current source filter if set, otherwise default to "MANUAL" if likely context
                const refreshFilters = { ...filters };
                if (origenTipo) refreshFilters.origen_tipo = origenTipo;
                // If the user hasn't selected a specific origin, usually we want to see what we just created.
                // But for now, just refreshing with current view filters is safest.
                fetchReport(refreshFilters, selectedType).then(() => {
                    if (formMode === "edit" && selectedLicitacion?.id_convocatoria) {
                        setHighlightId(selectedLicitacion.id_convocatoria);
                    } else if (formMode === "create" && result.data?.id_convocatoria) {
                        // Optional: Highlight created item if returned
                        setHighlightId(result.data.id_convocatoria);
                    }
                });
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error saving:", error);
            throw error;
        } finally {
            setIsSaving(false);
        }
    };

    const handleConfirmDelete = async (authCode: string) => {
        if (!selectedLicitacion) return;

        setIsDeleting(true);
        try {
            const response = await fetch(`/api/licitaciones/${selectedLicitacion.id_convocatoria}/eliminar`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ authCode })
            });

            const result = await response.json();

            if (result.success) {
                alert("Licitación eliminada exitosamente");
                setIsDeleteModalOpen(false);
                // Refresh data
                fetchReport(filters, selectedType);
            } else {
                alert("Error al eliminar: " + result.error);
            }
        } catch (error) {
            console.error("Error deleting:", error);
            alert("Error al eliminar la licitación");
        } finally {
            setIsDeleting(false);
        }
    };

    // Selection Handlers
    const toggleSelect = (id: number) => {
        const newSelected = new Set(selectedIds);
        if (newSelected.has(id)) {
            newSelected.delete(id);
        } else {
            newSelected.add(id);
        }
        setSelectedIds(newSelected);
    };

    const handleSelectAll = () => {
        if (selectedIds.size === reportData.length) {
            setSelectedIds(new Set());
        } else {
            setSelectedIds(new Set(reportData.map((d) => d.id_convocatoria)));
        }
    };

    const handleExport = async (format: "pdf" | "excel" | "csv") => {
        if (reportData.length === 0) {
            alert("No hay datos para exportar. Genera un reporte primero.");
            return;
        }

        setExporting(true);

        try {
            const dataToExport = selectedIds.size > 0
                ? reportData.filter(item => selectedIds.has(item.id_convocatoria))
                : reportData;

            const exportData = {
                columns: getColumns(),
                data: dataToExport,
                title: getReportTitle() + (selectedIds.size > 0 ? ` (Selección: ${selectedIds.size})` : ""),
                subtitle: getReportSubtitle(),
            };

            switch (format) {
                case "pdf":
                    exportToPDF(exportData);
                    break;
                case "excel":
                    exportToExcel(exportData);
                    break;
                case "csv":
                    exportToCSV(exportData);
                    break;
            }
        } catch (error) {
            console.error(`Error exportando a ${format}:`, error);
            alert(`Error al exportar a ${format.toUpperCase()}`);
        } finally {
            setExporting(false);
        }
    };

    const getColumns = () => {
        return allPersonalizedColumns.filter(c => visibleColumns.includes(c.key));
    };

    const getReportTitle = () => "Reporte de Gestión Manual";
    const getReportSubtitle = () => {
        const parts = [];
        if (filters.search) parts.push(`Búsqueda: ${filters.search}`);
        if (filters.departamento) parts.push(`Dpto: ${filters.departamento}`);
        if (origenTipo) parts.push(`Origen: ${origenTipo}`);
        return parts.join(" | ");
    };

    return (
        <div className="mx-auto max-w-7xl">
            {/* Filtros de Búsqueda */}
            <div className="mb-6">
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
                    <SearchFiltersComponent
                        onFilterChange={setFilters}
                        showTitle={true}
                        collapsible={true}
                        customTitle="Gestión Manual de Licitaciones"
                        customDescription="Busca, filtra y gestiona licitaciones manualmente con controles avanzados"
                        onClear={() => setOrigenTipo('')}
                    />
                </div>
            </div>

            {/* Barra de Acción Unificada */}
            <div className="mb-8">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between bg-white dark:bg-gray-900 p-2 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm">
                    {/* Izquierda: Contador + Buscar */}
                    <div className="flex flex-col sm:flex-row items-center gap-3 w-full lg:w-auto">

                        {/* Contador discreto - Movido al inicio izquierda */}
                        {paginationData.total > 0 && (
                            <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700">
                                <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Total:</span>
                                <span className="text-sm font-bold text-gray-900 dark:text-white">{paginationData.total}</span>
                            </div>
                        )}

                        {/* Botón Buscar */}
                        <button
                            onClick={handleGenerateReport}
                            disabled={loading}
                            className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-2 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-all hover:bg-blue-700 hover:shadow-blue-500/30 focus:outline-none focus:ring-4 focus:ring-blue-500/30 disabled:cursor-not-allowed disabled:opacity-50 w-full lg:w-auto min-w-[120px]"
                            title="Aplicar todos los filtros"
                        >
                            {loading ? (
                                <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            ) : (
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                            )}
                            <span>Buscar</span>
                        </button>
                    </div>

                    {/* Derecha: Nueva Licitación + Tabs */}
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center w-full lg:w-auto">

                        {/* Botón Principal: Nueva Licitación - Primero en la derecha */}
                        <div className="w-full sm:w-auto">
                            <AddLicitacionButton onClick={handleCreate} />
                        </div>

                        <div className="h-8 w-px bg-gray-200 dark:bg-gray-700 hidden sm:block mx-1"></div>

                        {/* Segmented Control (Tabs) - Al final a la derecha */}
                        {/* Botón Interactivo de Origen (Dropdown Personalizado) */}
                        {/* Botón Interactivo de Origen (Dropdown Personalizado) */}
                        <div className="relative">
                            <>
                                {/* Backdrop invisible para cerrar al hacer clic fuera */}
                                {isOriginDropdownOpen && (
                                    <div className="fixed inset-0 z-10" onClick={() => setIsOriginDropdownOpen(false)}></div>
                                )}

                                <button
                                    onClick={() => setIsOriginDropdownOpen(!isOriginDropdownOpen)}
                                    className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-all dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 min-w-[160px] justify-between relative z-20"
                                >
                                    <div className="flex items-center gap-2">
                                        <svg className="w-5 h-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={(originOptions.find(o => o.id === origenTipo) || originOptions[0]).icon} />
                                        </svg>
                                        <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{(originOptions.find(o => o.id === origenTipo) || originOptions[0]).label}</span>
                                    </div>
                                    <svg className={`w-4 h-4 text-gray-400 transition-transform ${isOriginDropdownOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </button>

                                {isOriginDropdownOpen && (
                                    <div className="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-100 dark:border-gray-700 py-1 z-30 animate-in fade-in zoom-in-95 duration-100 origin-top-right">
                                        {originOptions.map((type) => (
                                            <button
                                                key={type.id}
                                                onClick={() => {
                                                    setOrigenTipo(type.id);
                                                    fetchReport(filters, selectedType, type.id);
                                                    setIsOriginDropdownOpen(false);
                                                }}
                                                className={`
                                                    flex items-center gap-3 w-full px-4 py-2.5 text-sm transition-colors
                                                    ${origenTipo === type.id
                                                        ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
                                                        : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700/50'
                                                    }
                                                `}
                                            >
                                                <svg className={`w-4 h-4 ${origenTipo === type.id ? 'text-blue-500' : 'text-gray-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={type.icon} />
                                                </svg>
                                                {type.label}
                                                {origenTipo === type.id && (
                                                    <svg className="w-4 h-4 ml-auto text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                                    </svg>
                                                )}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </>
                        </div>
                    </div>
                </div>
            </div>

            {/* Resultados */}
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                {reportData.map((licitacion) => (
                    <LicitacionCard
                        key={licitacion.id_convocatoria}
                        id={`licitacion-${licitacion.id_convocatoria}`}
                        className={highlightId === licitacion.id_convocatoria ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-lg scale-[1.01]' : ''}
                        licitacion={licitacion as Licitacion}
                        showDownload={false}
                        showMenu={true}
                        onEdit={handleEdit}
                        onDelete={handleDelete}
                    />
                ))}
            </div>

            {/* Paginación */}
            {selectedType === 'personalizado' && paginationData.totalPages > 1 && (
                <div className="flex justify-center items-center gap-4 mt-8 pb-8">
                    <button
                        onClick={() => handlePageChange(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
                    >
                        Anterior
                    </button>

                    <span className="text-sm text-gray-600 dark:text-gray-400">
                        Página <span className="font-semibold text-gray-900 dark:text-white">{currentPage}</span> de <span className="font-semibold">{paginationData.totalPages}</span>
                        <span className="ml-2 text-xs text-gray-500">({paginationData.total} items)</span>
                    </span>

                    <button
                        onClick={() => handlePageChange(currentPage + 1)}
                        disabled={currentPage === paginationData.totalPages}
                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
                    >
                        Siguiente
                    </button>
                </div>
            )}

            {/* Modals */}
            <LicitacionFormModal
                isOpen={isFormModalOpen}
                onClose={() => setIsFormModalOpen(false)}
                onSave={handleSave}
                licitacion={selectedLicitacion}
                mode={formMode}
            />

            <DeleteConfirmationModal
                isOpen={isDeleteModalOpen}
                onClose={() => setIsDeleteModalOpen(false)}
                onConfirm={handleConfirmDelete}
                licitacion={selectedLicitacion}
                isDeleting={isDeleting}
            />
        </div >
    );
}

export default function GestionManualPage() {
    return (
        <React.Suspense fallback={<div className="flex h-screen items-center justify-center">Cargando gestión...</div>}>
            <GestionManualContent />
        </React.Suspense>
    );
}
