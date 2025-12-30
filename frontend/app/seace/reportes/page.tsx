"use client";

import React, { useState } from "react";
import { ReportSelector } from "@/components/reports/ReportSelector";
import { SearchFiltersComponent } from "@/components/search/SearchFilters";
import { ReportTable } from "@/components/reports/ReportTable";
import { ExportButtons } from "@/components/reports/ExportButtons";
import { exportToPDF, exportToExcel, exportToCSV } from "@/lib/exportUtils";
import type { ReportType, SearchFilters } from "@/types/licitacion";

export default function ReportesPage() {
    const [selectedType, setSelectedType] = useState<ReportType>("entidad");
    const [filters, setFilters] = useState<SearchFilters>({});
    const [reportData, setReportData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [exporting, setExporting] = useState(false);

    const handleGenerateReport = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/reportes/generar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tipo: selectedType,
                    filtros: filters
                })
            });

            const result = await response.json();

            if (result.success) {
                setReportData(result.data);
            } else {
                console.error("Error en respuesta:", result.error);
                alert("Error al generar el reporte");
            }
        } catch (error) {
            console.error("Error generando reporte:", error);
            alert("Error al conectar con el servidor");
        } finally {
            setLoading(false);
        }
    };

    const getColumns = () => {
        switch (selectedType) {
            case "entidad":
                return [
                    { key: "nombre", label: "Entidad Financiera" },
                    { key: "garantias", label: "Garantías" },
                    { key: "monto", label: "Monto Total" },
                    { key: "departamentos", label: "Departamentos" },
                ];
            case "departamento":
                return [
                    { key: "nombre", label: "Departamento" },
                    { key: "garantias", label: "Licitaciones" },
                    { key: "monto", label: "Monto Total" },
                    { key: "categorias", label: "Categorías" },
                ];
            case "categoria":
                return [
                    { key: "nombre", label: "Categoría" },
                    { key: "garantias", label: "Licitaciones" },
                    { key: "monto", label: "Monto Total" },
                    { key: "departamentos", label: "Departamentos" },
                ];
            case "estado":
                return [
                    { key: "nombre", label: "Estado" },
                    { key: "garantias", label: "Licitaciones" },
                    { key: "monto", label: "Monto Total" },
                    { key: "departamentos", label: "Departamentos" },
                ];
            default:
                return [
                    { key: "nombre", label: "Descripción" },
                    { key: "garantias", label: "Garantías" },
                    { key: "monto", label: "Monto" },
                    { key: "departamento", label: "Departamento" },
                ];
        }
    };

    const handleExport = async (format: "pdf" | "excel" | "csv") => {
        if (reportData.length === 0) {
            alert("No hay datos para exportar. Genera un reporte primero.");
            return;
        }

        setExporting(true);

        try {
            const exportData = {
                columns: getColumns(),
                data: reportData,
                title: `Reporte por ${selectedType.charAt(0).toUpperCase() + selectedType.slice(1)}`,
                subtitle: `Generado el ${new Date().toLocaleDateString()}`
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

    return (
        // Updated Backgrounds
        <div className="min-h-screen bg-slate-50 dark:bg-[#0b122b] p-4 sm:p-6 lg:p-8 transition-colors duration-300">
            <div className="mx-auto max-w-7xl space-y-8">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
                        Generador de Reportes
                    </h1>
                    <p className="mt-2 text-slate-600 dark:text-slate-400">
                        Crea reportes detallados y expórtalos en múltiples formatos.
                    </p>
                </div>

                {/* Selector */}
                <ReportSelector
                    selectedType={selectedType}
                    onTypeChange={(type) => {
                        setSelectedType(type);
                        setReportData([]);
                    }}
                />

                {/* Filters */}
                {/* Updated Theme */}
                {/* Filters */}
                {/* Updated Theme */}
                <div className="rounded-2xl border border-slate-200/60 bg-white p-6 shadow-sm dark:border-white/5 dark:bg-[#111c44] backdrop-blur-xl">
                    <SearchFiltersComponent onFilterChange={setFilters} />
                </div>

                {/* Actions */}
                <div className="flex flex-wrap items-center justify-between gap-4">
                    <button
                        onClick={handleGenerateReport}
                        disabled={loading}
                        className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition-all hover:bg-indigo-700 hover:shadow-indigo-500/50 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                        {loading ? "Generando..." : "Generar Reporte"}
                    </button>

                    {reportData.length > 0 && (
                        <ExportButtons
                            onExport={handleExport}
                            loading={exporting}
                            disabled={loading}
                        />
                    )}
                </div>

                {/* Table */}
                <ReportTable
                    data={reportData}
                    columns={getColumns()}
                    loading={loading}
                />
            </div>
        </div>
    );
}
