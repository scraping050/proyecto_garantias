"use client";
import { useState, useEffect } from "react";
import { MoreDotIcon } from "@/icons";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import PeruMap from "./PeruMap";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Interface for department data
interface ProvinceData {
    provincia: string;
    total: number;
    monto_total: string;
}

export default function DemographicCard() {
    const [departments, setDepartments] = useState<DepartmentData[]>([]);
    const [provinces, setProvinces] = useState<ProvinceData[]>([]);
    const [loading, setLoading] = useState(true);
    const [loadingProvinces, setLoadingProvinces] = useState(false);

    // State for selection
    const [selectedDept, setSelectedDept] = useState<string | null>(null);
    const [showAll, setShowAll] = useState(false);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    useEffect(() => {
        const fetchDepartments = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/reportes/por-departamento`);
                const data: ApiResponse = await response.json();

                if (data.success && data.data && data.data.departamentos) {
                    setDepartments(data.data.departamentos);
                }
            } catch (error) {
                console.error('Error fetching departments:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchDepartments();
    }, []);

    // Function to fetch provinces when a department is selected
    const fetchProvinces = async (deptName: string) => {
        setLoadingProvinces(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/reportes/por-provincia/${encodeURIComponent(deptName)}`);
            const data = await response.json();
            if (data.success && data.data && data.data.provincias) {
                setProvinces(data.data.provincias);
            }
        } catch (error) {
            console.error("Error fetching provinces:", error);
        } finally {
            setLoadingProvinces(false);
        }
    };

    // Handler for map selection
    const handleMapSelect = (dept: string | null) => {
        setSelectedDept(dept);
        if (dept) {
            fetchProvinces(dept);
        } else {
            setProvinces([]);
        }
    };

    // Derived state for display
    const isDrillDown = !!selectedDept;

    // Base for percentage calculation
    // If National view (default): Total = Sum of all departments
    // If Province view (drilldown): Total = Total of that specific department (or sum of its provinces)
    const NATIONAL_TOTAL = departments.reduce((sum, d) => sum + d.total, 0);

    const currentTotal = isDrillDown
        ? (departments.find(d => d.departamento === selectedDept)?.total || 0)
        : NATIONAL_TOTAL;

    // Items to display (Departments or Provinces)
    const itemsToDisplay = isDrillDown ? provinces : departments;

    // Pagination / Show More logic
    const visibleItems = showAll ? itemsToDisplay : itemsToDisplay.slice(0, 10);

    const getPercentage = (value: number) => {
        return currentTotal > 0 ? Math.round((value / currentTotal) * 100) : 0;
    };

    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] sm:p-6 transition-all duration-300">
            <div className="flex justify-between items-start">
                <div>
                    <h3 className="text-lg font-bold text-gray-800 dark:text-white uppercase tracking-tight">
                        {isDrillDown ? `Licitaciones en ${selectedDept}` : 'Licitaciones por Departamento'}
                    </h3>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        {isDrillDown
                            ? `Distribución provincial en ${selectedDept}`
                            : 'Distribución nacional de licitaciones'}
                    </p>
                </div>

                <div className="relative">
                    <button
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                        className="dropdown-toggle p-1 hover:bg-gray-100 rounded-full dark:hover:bg-gray-800 transition-colors"
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

            {/* Map Section */}
            <div className="mt-6 mb-8">
                <PeruMap departments={departments} onSelect={handleMapSelect} />
            </div>

            {/* Data List */}
            <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                {loading || (isDrillDown && loadingProvinces) ? (
                    <div className="py-10 text-center text-gray-500 dark:text-gray-400 animate-pulse">
                        Cargando datos...
                    </div>
                ) : visibleItems.length === 0 ? (
                    <div className="text-center text-gray-500 py-4">No hay datos disponibles.</div>
                ) : (
                    visibleItems.map((item, index) => {
                        // Determine name/total based on type
                        const name = (item as any).departamento || (item as any).provincia;
                        const total = item.total;

                        const percentage = getPercentage(total);
                        const position = index + 1;

                        return (
                            <div key={name} className="space-y-2 group">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="flex h-8 w-8 items-center justify-center rounded-lg text-xs font-bold transition-colors bg-blue-500/10 text-blue-500">
                                            #{position}
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-gray-700 dark:text-white/90">
                                                {name}
                                            </p>
                                            <p className="text-[10px] uppercase font-semibold text-gray-400 dark:text-gray-500 tracking-wider">
                                                {total.toLocaleString()} Licitaciones
                                            </p>
                                        </div>
                                    </div>
                                    <span className="text-sm font-bold text-gray-700 dark:text-white/80 font-mono">
                                        {percentage}%
                                    </span>
                                </div>

                                {/* Progress Bar */}
                                <div className="h-1.5 w-full overflow-hidden rounded-full bg-gray-100 dark:bg-gray-800">
                                    <div
                                        className="h-full rounded-full transition-all duration-500 ease-out bg-blue-500"
                                        style={{ width: `${percentage}%` }}
                                    />
                                </div>
                            </div>
                        );
                    })
                )}
            </div>

            {/* Footer */}
            <div className="mt-6 border-t border-gray-200 pt-4 dark:border-gray-800">
                <div className="flex justify-between items-center">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wider">
                        {isDrillDown ? 'Vista Provincial' : 'Vista Nacional'}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                        Mostrando {visibleItems.length} de {itemsToDisplay.length} {isDrillDown ? 'provincias' : 'departamentos'}
                    </div>
                </div>
            </div>
        </div>
    );
}
