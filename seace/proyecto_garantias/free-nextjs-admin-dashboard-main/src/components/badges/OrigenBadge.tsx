"use client";
import React from "react";

interface OrigenBadgeProps {
    origen?: 'ETL' | 'MANUAL' | 'MODIFICADO';
    estado?: 'ACTIVO' | 'ELIMINADO';
    size?: 'sm' | 'md' | 'lg';
}

const ORIGEN_COLORS = {
    ETL: {
        bg: 'bg-blue-50 dark:bg-blue-950/20',
        text: 'text-blue-700 dark:text-blue-400',
        border: 'border-blue-200 dark:border-blue-800',
        icon: '🔵',
        label: 'ETL'
    },
    MANUAL: {
        bg: 'bg-emerald-50 dark:bg-emerald-950/20',
        text: 'text-emerald-700 dark:text-emerald-400',
        border: 'border-emerald-200 dark:border-emerald-800',
        icon: '🟢',
        label: 'MANUAL'
    },
    MODIFICADO: {
        bg: 'bg-amber-50 dark:bg-amber-950/20',
        text: 'text-amber-700 dark:text-amber-400',
        border: 'border-amber-200 dark:border-amber-800',
        icon: '🟡',
        label: 'MODIFICADA'
    },
    ELIMINADO: {
        bg: 'bg-red-50 dark:bg-red-950/20',
        text: 'text-red-700 dark:text-red-400',
        border: 'border-red-200 dark:border-red-800',
        icon: '🔴',
        label: 'ELIMINADA'
    }
};

const SIZE_CLASSES = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-xs',
    lg: 'px-4 py-1.5 text-sm'
};

export function OrigenBadge({ origen = 'ETL', estado = 'ACTIVO', size = 'md' }: OrigenBadgeProps) {
    // Si está eliminado, mostrar badge de eliminado
    const badgeType = estado === 'ELIMINADO' ? 'ELIMINADO' : origen;
    const colors = ORIGEN_COLORS[badgeType];
    const sizeClass = SIZE_CLASSES[size];

    return (
        <div className={`
            inline-flex items-center gap-1.5 rounded-full
            ${colors.bg} ${colors.text} ${colors.border} border
            ${sizeClass}
            font-medium
            transition-all duration-200
            hover:scale-105 hover:shadow-sm
        `}>
            <span className="text-sm leading-none">{colors.icon}</span>
            <span className="leading-none">{colors.label}</span>
        </div>
    );
}
