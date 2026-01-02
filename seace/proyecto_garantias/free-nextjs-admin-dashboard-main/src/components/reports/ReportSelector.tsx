import React from "react";
import { ReportType } from "@/types/licitacion";

interface ReportSelectorProps {
    selectedType: ReportType;
    onTypeChange: (type: ReportType) => void;
}

export const ReportSelector: React.FC<ReportSelectorProps> = ({
    selectedType,
    onTypeChange,
}) => {
    const reportTypes: { id: ReportType; label: string; description: string }[] = [
        {
            id: "entidad",
            label: "Por Entidad Financiera",
            description: "Análisis de garantías por banco o aseguradora",
        },
        {
            id: "departamento",
            label: "Por Departamento",
            description: "Distribución geográfica de licitaciones",
        },
        {
            id: "categoria",
            label: "Por Categoría",
            description: "Desglose por rubro o sector",
        },
        {
            id: "estado",
            label: "Por Estado",
            description: "Resumen de estados de los procesos",
        },
        {
            id: "personalizado",
            label: "Lista Detallada",
            description: "Reporte fila por fila con columnas personalizables",
        },
    ];

    return (
        <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {reportTypes.map((type) => (
                <button
                    key={type.id}
                    onClick={() => onTypeChange(type.id)}
                    className={`flex flex-col items-start gap-2 rounded-xl border p-4 text-left transition-all hover:shadow-md ${selectedType === type.id
                            ? "border-blue-500 bg-blue-50 ring-1 ring-blue-500 dark:border-blue-400 dark:bg-blue-900/20"
                            : "border-gray-200 bg-white hover:border-gray-300 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-gray-700"
                        }`}
                >
                    <span
                        className={`font-semibold ${selectedType === type.id
                                ? "text-blue-700 dark:text-blue-300"
                                : "text-gray-900 dark:text-gray-100"
                            }`}
                    >
                        {type.label}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                        {type.description}
                    </span>
                </button>
            ))}
        </div>
    );
};
