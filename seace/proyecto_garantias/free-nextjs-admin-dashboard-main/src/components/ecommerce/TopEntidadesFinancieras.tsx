"use client";
import { useEffect, useState } from "react";
import { MoreDotIcon } from "@/icons";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Define the TypeScript interface for financial entities
interface FinancialEntity {
    entidad_financiera: string;
    total: number;
    monto_total: string;
    departamentos_atendidos: number;
    categorias_atendidas: number;
}

// Mapping of full names to abbreviated names
const getAbreviacion = (nombre: string): string => {
    const nombreUpper = nombre.toUpperCase();

    // Check for cooperatives FIRST (before checking for "CREDITO" which would match BCP)
    if (nombreUpper.includes('COOPERATIVA')) return 'Coop. San Lorenzo';

    if (nombreUpper.includes('AVLA')) return 'AVLA Perú';
    if (nombreUpper.includes('CESCE')) return 'CESCE Perú';
    if (nombreUpper.includes('BBVA')) return 'BBVA Perú';
    if (nombreUpper.includes('CREDITO') || nombreUpper.includes('BCP')) return 'BCP';
    if (nombreUpper.includes('CRECER')) return 'Crecer Seguros';
    if (nombreUpper.includes('SCOTIABANK')) return 'Scotiabank';
    if (nombreUpper.includes('INSUR')) return 'Insur Seguros';
    if (nombreUpper.includes('INTERAMERICANO')) return 'Interamericano';
    if (nombreUpper.includes('CITIBANK')) return 'Citibank';
    if (nombreUpper.includes('INTERNACIONAL')) return 'Internacional';
    if (nombreUpper.includes('FOGAPI')) return 'FOGAPI';
    if (nombreUpper.includes('SANTANDER')) return 'Santander';
    if (nombreUpper.includes('CMAC')) {
        const parts = nombreUpper.split(' ');
        const cityIndex = parts.findIndex(p => p === 'CMAC') + 1;
        if (cityIndex < parts.length) {
            const city = parts[cityIndex];
            return `CMAC ${city.charAt(0)}${city.slice(1).toLowerCase()}`;
        }
        return 'CMAC';
    }
    if (nombreUpper.includes('PICHINCHA')) return 'Pichincha';
    if (nombreUpper.includes('MAPFRE')) return 'Mapfre';
    if (nombreUpper.includes('POSITIVA')) return 'La Positiva';

    // Default: take first 20 characters
    return nombre.substring(0, 20) + (nombre.length > 20 ? '...' : '');
};

// Function to get coverage badge color
const getCoverageBadge = (departamentos: number): string => {
    if (departamentos >= 24) return "bg-green-500/10 text-green-500"; // Nacional
    if (departamentos >= 15) return "bg-blue-500/10 text-blue-500";   // Regional
    return "bg-gray-500/10 text-gray-500";                            // Local
};

const getCoverageText = (departamentos: number): string => {
    if (departamentos >= 24) return "Nacional";
    if (departamentos >= 15) return "Regional";
    return "Local";
};

// Format currency
const formatMonto = (monto: string | number): string => {
    const num = typeof monto === 'string' ? parseFloat(monto) : monto;
    if (isNaN(num)) return 'S/ 0';

    if (num >= 1000000000) {
        return `S/ ${(num / 1000000000).toFixed(1)}B`;
    } else if (num >= 1000000) {
        return `S/ ${(num / 1000000).toFixed(1)}M`;
    }
    return `S/ ${(num / 1000).toFixed(0)}K`;
};

export default function TopEntidadesFinancieras() {
    const [entities, setEntities] = useState<FinancialEntity[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showAll, setShowAll] = useState(false);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/reportes/por-entidad-financiera`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data: any = await response.json();
                if (data.success && data.data && data.data.entidades) {
                    setEntities(data.data.entidades);
                } else {
                    throw new Error('Failed to fetch data');
                }
            } catch (err) {
                console.error('Error fetching financial entities:', err);
                setError(err instanceof Error ? err.message : 'Unknown error');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Show only first 10 entities unless showAll is true
    const displayedEntities = showAll ? entities : entities.slice(0, 10);

    if (loading) {
        return (
            <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
                <div className="flex items-center justify-center py-8">
                    <div className="text-gray-500 dark:text-gray-400">Cargando...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-4 pb-3 pt-4 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">
                <div className="flex items-center justify-center py-8">
                    <div className="text-red-500">Error: {error}</div>
                </div>
            </div>
        );
    }

    return (
        <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-gray-200 px-5 py-4 dark:border-gray-800 sm:px-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                    Top Entidades Financieras
                </h3>
                <div className="relative">
                    <button
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                        className="dropdown-toggle"
                    >
                        <MoreDotIcon className="text-gray-400 hover:text-gray-700 dark:hover:text-gray-300" />
                    </button>

                    {isDropdownOpen && (
                        <div className="absolute right-full top-0 z-50 mr-2 w-48 rounded-lg border border-gray-200 bg-white p-2 shadow-lg dark:border-gray-700 dark:bg-gray-800">
                            <button
                                onClick={() => {
                                    setShowAll(!showAll);
                                    setIsDropdownOpen(false);
                                }}
                                className="flex w-full items-center rounded-lg px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
                            >
                                {showAll ? 'Ver Menos' : 'Ver Más'}
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Table Header */}
            <div className="grid grid-cols-4 border-b border-gray-200 px-5 py-3 dark:border-gray-800 sm:px-6">
                <div className="text-xs font-medium text-gray-400 dark:text-gray-500">
                    ENTIDAD
                </div>
                <div className="text-center text-xs font-medium text-gray-400 dark:text-gray-500">
                    GARANTÍAS
                </div>
                <div className="text-center text-xs font-medium text-gray-400 dark:text-gray-500">
                    MONTO
                </div>
                <div className="text-center text-xs font-medium text-gray-400 dark:text-gray-500">
                    COBERTURA
                </div>
            </div>

            {/* Table Rows */}
            <div className="divide-y divide-gray-100 dark:divide-white/[0.05]">
                {displayedEntities.map((entity, index) => (
                    <div
                        key={index}
                        className="grid grid-cols-4 items-center px-5 py-4 transition-colors hover:bg-gray-50 dark:hover:bg-white/[0.02] sm:px-6"
                        title={entity.entidad_financiera} // Tooltip with full name
                    >
                        {/* Entity Name */}
                        <div className="flex items-center gap-3">
                            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/10 text-blue-500">
                                <span className="text-sm font-semibold">
                                    {getAbreviacion(entity.entidad_financiera).substring(0, 2).toUpperCase()}
                                </span>
                            </div>
                            <div>
                                <p className="text-sm font-medium text-gray-700 dark:text-white/80">
                                    {getAbreviacion(entity.entidad_financiera)}
                                </p>
                                <p className="text-xs text-gray-400 dark:text-gray-500">
                                    {entity.departamentos_atendidos} Depts.
                                </p>
                            </div>
                        </div>

                        {/* Guarantees */}
                        <div className="text-center">
                            <p className="text-sm font-medium text-gray-700 dark:text-white/80">
                                {entity.total.toLocaleString()}
                            </p>
                        </div>

                        {/* Amount */}
                        <div className="text-center">
                            <p className="text-sm font-medium text-gray-700 dark:text-white/80">
                                {formatMonto(entity.monto_total)}
                            </p>
                        </div>

                        {/* Coverage Badge */}
                        <div className="flex justify-center">
                            <span className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${getCoverageBadge(entity.departamentos_atendidos)}`}>
                                {getCoverageText(entity.departamentos_atendidos)}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer */}
            <div className="border-t border-gray-200 px-5 py-4 dark:border-gray-800 sm:px-6">
                <div className="text-sm text-gray-500 dark:text-gray-400">
                    Mostrando {displayedEntities.length} de {entities.length} entidades
                </div>
            </div>
        </div>
    );
}
