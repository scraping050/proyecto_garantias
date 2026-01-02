"use client";
import React from "react";

interface AddLicitacionButtonProps {
    onClick: () => void;
}

export const AddLicitacionButton: React.FC<AddLicitacionButtonProps> = ({ onClick }) => {
    return (
        <button
            onClick={onClick}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-green-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-green-500/20 transition-all hover:bg-green-700 hover:shadow-green-500/30 focus:outline-none focus:ring-4 focus:ring-green-500/30"
        >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                />
            </svg>
            Nueva Licitación
        </button>
    );
};
