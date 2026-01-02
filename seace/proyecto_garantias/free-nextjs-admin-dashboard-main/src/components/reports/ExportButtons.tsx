import React from "react";

interface ExportButtonsProps {
    onExport: (format: "pdf" | "excel" | "csv") => void;
    loading: boolean;
    disabled?: boolean;
}

export const ExportButtons: React.FC<ExportButtonsProps> = ({
    onExport,
    loading,
    disabled,
}) => {
    const btnClass =
        "inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition-all focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50";

    return (
        <div className="flex flex-wrap items-center gap-2">
            <span className="mr-2 text-sm font-medium text-gray-500 dark:text-gray-400">
                Exportar:
            </span>
            <button
                onClick={() => onExport("pdf")}
                disabled={disabled || loading}
                className={`${btnClass} border-red-200 bg-red-50 text-red-700 hover:border-red-300 hover:bg-red-100 focus:ring-red-500 dark:border-red-900/30 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/40`}
            >
                <svg
                    className="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                    />
                </svg>
                PDF
            </button>
            <button
                onClick={() => onExport("excel")}
                disabled={disabled || loading}
                className={`${btnClass} border-green-200 bg-green-50 text-green-700 hover:border-green-300 hover:bg-green-100 focus:ring-green-500 dark:border-green-900/30 dark:bg-green-900/20 dark:text-green-400 dark:hover:bg-green-900/40`}
            >
                <svg
                    className="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                </svg>
                Excel
            </button>
            <button
                onClick={() => onExport("csv")}
                disabled={disabled || loading}
                className={`${btnClass} border-gray-200 bg-white text-gray-700 hover:bg-gray-50 focus:ring-gray-500 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700`}
            >
                <svg
                    className="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                </svg>
                CSV
            </button>
        </div>
    );
};
