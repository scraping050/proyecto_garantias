"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import type { ReportType, SearchFilters, Licitacion } from "@/types/licitacion";
import { SearchFiltersComponent } from "@/components/search/SearchFilters";
import { ReportSelector } from "@/components/reports/ReportSelector";
import { ReportTable } from "@/components/reports/ReportTable";
import { LicitacionCard } from "@/components/search/LicitacionCard";
import { ExportButtons } from "@/components/reports/ExportButtons";
import { ColumnSelector } from "@/components/reports/ColumnSelector";
import { exportToPDF, exportToExcel, exportToCSV } from "@/lib/exportUtils";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Helper hook
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

function ReportesContent() {
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

    // Debounce filters
    const debouncedFilters = useDebounce(filters, 800);

    // Auto-fetch on debounce change
    useEffect(() => {
        // Skip initial mount if desired, but here we generally want to search if filters exist
        // or just on any change.
        if (hasInitialFetch) {
            handleGenerateReport();
        }
    }, [debouncedFilters]);

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
        // Don't auto-fetch here, user clicks "Generate"
    };

    const handleGenerateReport = async () => {
        setSelectedIds(new Set()); // Reset selection on new search
        updateURL(filters, selectedType);
        fetchReport(filters, selectedType);
    };

    const fetchReport = async (currentFilters: SearchFilters, currentType: ReportType) => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/reportes/generar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tipo: currentType,
                    filtros: currentFilters
                })
            });

            const result = await response.json();

            if (result.success) {
                // Deduplicate items by id_convocatoria to prevent React key errors
                const uniqueItems = Array.from(
                    new Map((result.data || []).map((item: any) => [item.id_convocatoria, item])).values()
                );
                setReportData(uniqueItems);

                // Auto-select all items by default as requested
                setSelectedIds(new Set(uniqueItems.map((item: any) => item.id_convocatoria)));
            } else {
                console.error("Error en respuesta:", result.error);
                alert("Error al generar el reporte");
            }
        } catch (error) {
            console.error("Error generando reporte:", error);
            alert("Error al conectar con el servidor (Verifique que el backend esté corriendo)");
        } finally {
            setLoading(false);
        }
    };

    // Auto-fetch if there are params on mount (e.g. back navigation)
    useEffect(() => {
        const hasParams = Array.from(searchParams.keys()).length > 0;
        if (hasParams && !hasInitialFetch) {
            fetchReport(filters, selectedType);
            setHasInitialFetch(true);
        }
    }, [searchParams]);

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
            // Filter data if selection is active
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

    const getReportTitle = () => {
        const titles: Record<string, string> = {
            entidad: "Reporte por Entidad Financiera",
            departamento: "Reporte por Departamento",
            categoria: "Reporte por Categoría",
            estado: "Reporte por Estado",
            personalizado: "Reporte Detallado Personalizado",
        };
        return titles[selectedType] || "Reporte";
    };

    const getReportSubtitle = () => {
        const parts = [];
        if (filters.departamento) parts.push(`Departamento: ${filters.departamento}`);
        if (filters.categoria) parts.push(`Categoría: ${filters.categoria}`);
        if (filters.year) parts.push(`Año: ${filters.year}`);
        return parts.length > 0 ? parts.join(" | ") : undefined;
    };

    const getColumns = () => {
        switch (selectedType) {
            case "entidad":
                return [
                    { key: "nombre", label: "Entidad Financiera" },
                    { key: "total", label: "# Garantías" },
                    { key: "monto_total", label: "Monto Total" },
                    { key: "departamentos_atendidos", label: "Departamentos" },
                ];
            case "departamento":
                return [
                    { key: "departamento", label: "Departamento" },
                    { key: "total", label: "# Licitaciones" },
                    { key: "monto_total", label: "Monto Total" },
                ];
            case "categoria":
                return [
                    { key: "categoria", label: "Categoría" },
                    { key: "total", label: "# Licitaciones" },
                    { key: "monto_total", label: "Monto Total" },
                ];
            case "estado":
                return [
                    { key: "estado", label: "Estado" },
                    { key: "total", label: "# Licitaciones" },
                    { key: "retencion", label: "# Retenciones" },
                ];
            case "personalizado":
                return allPersonalizedColumns.filter(col => visibleColumns.includes(col.key));
            default:
                return [];
        }
    };

    const toggleColumn = (key: string) => {
        setVisibleColumns(prev =>
            prev.includes(key)
                ? prev.filter(c => c !== key)
                : [...prev, key]
        );
    };

    return (
        <div className="mx-auto max-w-7xl">
            {/* Header Removed as requested */}

            {/* Selector de tipo de reporte REMOVED as requested */}

            {/* Filtros */}
            <div className="mb-6">
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
                    <div className="mb-6">
                        <SearchFiltersComponent
                            onFilterChange={setFilters}
                            showTitle={true}
                            collapsible={true}
                            customTitle="Generador de Reportes"
                            customDescription="Genera reportes personalizados con filtros avanzados y exporta a múltiples formatos"
                        />
                    </div>

                    {/* Column Selector REMOVED as requested */}
                </div>
            </div>

            {/* Botón generar reporte y exportación */}
            <div className="mb-8 flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
                    <button
                        onClick={handleGenerateReport}
                        disabled={loading}
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-all hover:bg-blue-700 hover:shadow-blue-500/30 focus:ring-4 focus:ring-blue-500/30 disabled:cursor-not-allowed disabled:opacity-50 min-w-[200px]"
                    >
                        {loading ? (
                            <svg className="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        ) : (
                            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        )}
                        {loading ? "Generando..." : "Generar Vista Previa"}
                    </button>

                    {/* Result Count Badge */}
                    {!loading && reportData.length > 0 && (
                        <div className="flex items-center gap-2 animate-fade-in px-4 py-2 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700">
                            <div className="flex flex-col">
                                <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Resultados</span>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-xl font-bold text-gray-900 dark:text-white">{reportData.length}</span>
                                    <span className="text-xs text-gray-500 dark:text-gray-400">encontrados</span>
                                </div>
                            </div>
                            <div className="h-8 w-px bg-gray-200 dark:bg-gray-700 mx-2"></div>
                            <div className="flex flex-col">
                                <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Selección</span>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-xl font-bold text-blue-600 dark:text-blue-400">{selectedIds.size}</span>
                                    <span className="text-xs text-gray-500 dark:text-gray-400">items</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {reportData.length > 0 && (
                    <div className="flex items-center gap-4 animate-fade-in">
                        {/* Select All Toggle */}
                        {selectedType === "personalizado" && (
                            <button
                                onClick={handleSelectAll}
                                className="text-sm font-medium text-gray-600 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400"
                            >
                                {selectedIds.size === reportData.length ? "Deseleccionar Todos" : "Seleccionar Todos"}
                            </button>
                        )}

                        <ExportButtons
                            onExport={handleExport}
                            loading={exporting}
                            disabled={loading}
                        />
                    </div>
                )}
            </div>

            {/* Resultados */}
            {selectedType === "personalizado" ? (
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {reportData.map((licitacion) => (
                        <LicitacionCard
                            key={licitacion.id_convocatoria}
                            licitacion={licitacion as Licitacion}
                            isSelected={selectedIds.has(licitacion.id_convocatoria)}
                            onToggleSelect={toggleSelect}
                            showDownload={false}
                        />
                    ))}
                </div>
            ) : (
                <ReportTable
                    data={reportData}
                    columns={getColumns()}
                    loading={loading}
                />
            )}
        </div>
    );
}

export default function ReportesPage() {
    return (
        <React.Suspense fallback={<div className="flex h-screen items-center justify-center">Cargando reportes...</div>}>
            <ReportesContent />
        </React.Suspense>
    );
}
