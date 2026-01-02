import React from "react";

interface Column {
    key: string;
    label: string;
}

interface ColumnSelectorProps {
    allColumns: Column[];
    visibleColumns: string[];
    onToggleColumn: (key: string) => void;
}

export const ColumnSelector: React.FC<ColumnSelectorProps> = ({
    allColumns,
    visibleColumns,
    onToggleColumn,
}) => {
    return (
        <div className="mb-4">
            <h4 className="mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                Personalizar Columnas:
            </h4>
            <div className="flex flex-wrap gap-2">
                {allColumns.map((col) => (
                    <button
                        key={col.key}
                        onClick={() => onToggleColumn(col.key)}
                        className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors border ${visibleColumns.includes(col.key)
                                ? "bg-indigo-100 text-indigo-700 border-indigo-200 dark:bg-indigo-900/30 dark:text-indigo-300 dark:border-indigo-800/50"
                                : "bg-gray-50 text-gray-500 border-gray-200 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700"
                            }`}
                    >
                        {visibleColumns.includes(col.key) && (
                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                        )}
                        {col.label}
                    </button>
                ))}
            </div>
        </div>
    );
};
