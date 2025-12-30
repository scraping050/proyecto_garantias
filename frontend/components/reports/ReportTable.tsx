import React from "react";

interface Column {
    key: string;
    label: string;
}

interface Props {
    data: any[];
    columns: Column[];
    loading: boolean;
}

export const ReportTable: React.FC<Props> = ({ data, columns, loading }) => {
    if (loading) {
        return (
            <div className="mt-8 space-y-4">
                {[...Array(5)].map((_, i) => (
                    <div key={i} className="h-16 w-full animate-pulse rounded-xl bg-slate-200/50 dark:bg-slate-800/50" />
                ))}
            </div>
        );
    }

    if (data.length === 0) {
        return (
            <div className="mt-8 flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-white/50 p-12 text-center dark:border-slate-700 dark:bg-slate-900/50">
                <svg className="h-12 w-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="mt-4 text-base font-semibold text-slate-900 dark:text-white">Sin datos para mostrar</h3>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Genera un reporte para ver los resultados aquí.</p>
            </div>
        );
    }

    return (
        <div className="mt-8 overflow-hidden rounded-2xl border border-slate-200/60 bg-white shadow-sm dark:border-slate-700/60 dark:bg-slate-900/50 bg-backdrop-blur-xl">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-700">
                    <thead className="bg-slate-50 dark:bg-slate-800/50">
                        <tr>
                            {columns.map((col, idx) => (
                                <th
                                    key={idx}
                                    scope="col"
                                    className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400"
                                >
                                    {col.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 bg-white dark:divide-slate-700 dark:bg-transparent">
                        {data.map((row, rowIndex) => (
                            <tr
                                key={rowIndex}
                                className="transition-colors hover:bg-slate-50/50 dark:hover:bg-slate-800/30"
                            >
                                {columns.map((col, colIndex) => (
                                    <td key={colIndex} className="whitespace-nowrap px-6 py-4">
                                        <div className={`text-sm ${colIndex === 0
                                                ? "font-medium text-slate-900 dark:text-white"
                                                : "text-slate-500 dark:text-slate-400"
                                            }`}>
                                            {row[col.key]}
                                        </div>
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
