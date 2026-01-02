import React from "react";

interface Column {
    key: string;
    label: string;
}

interface ReportTableProps {
    data: any[];
    columns: Column[];
    loading: boolean;
}

export const ReportTable: React.FC<ReportTableProps> = ({
    data,
    columns,
    loading,
}) => {
    if (loading) {
        return (
            <div className="animate-pulse space-y-4">
                <div className="h-12 w-full rounded bg-gray-200 dark:bg-gray-800"></div>
                {[...Array(5)].map((_, i) => (
                    <div
                        key={i}
                        className="h-16 w-full rounded bg-gray-100 dark:bg-gray-900"
                    ></div>
                ))}
            </div>
        );
    }

    if (!data || data.length === 0) {
        return (
            <div className="flex h-64 flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-200 bg-gray-50 text-center dark:border-gray-800 dark:bg-gray-900/50">
                <p className="text-gray-500 dark:text-gray-400">
                    No hay datos para mostrar. Ajusta los filtros o genera el reporte.
                </p>
            </div>
        );
    }

    return (
        <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <div className="overflow-x-auto">
                <table className="w-full min-w-max table-auto text-left">
                    <thead>
                        <tr className="border-b border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-gray-800/50">
                            {columns.map((col) => (
                                <th
                                    key={col.key}
                                    className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400"
                                >
                                    {col.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                        {data.map((row, index) => (
                            <tr
                                key={index}
                                className="transition-colors hover:bg-gray-50 dark:hover:bg-gray-800/50"
                            >
                                {columns.map((col) => (
                                    <td
                                        key={col.key}
                                        className="whitespace-nowrap px-6 py-4 text-sm text-gray-900 dark:text-gray-100"
                                    >
                                        {formatValue(row[col.key], col.key)}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 text-xs text-gray-500 dark:border-gray-800 dark:bg-gray-800/50 dark:text-gray-400">
                Mostrando {data.length} registros
            </div>
        </div>
    );
};

import { formatEntityName } from "@/lib/formatUtils";

/* ... existing code ... */

const formatValue = (value: any, key: string) => {
    if (value === null || value === undefined) return "-";

    if (key === 'entidad' || key === 'entidad_financiera') {
        return formatEntityName(value);
    }

    if (key.includes("monto") || key === "amount") {
        /* ... existing code ... */
        return new Intl.NumberFormat("es-PE", {
            style: "currency",
            currency: "PEN",
        }).format(Number(value));
    }

    if (key.includes("fecha") || key.includes("date")) {
        try {
            return new Date(value).toLocaleDateString("es-PE");
        } catch (e) {
            return value;
        }
    }

    return value;
};
