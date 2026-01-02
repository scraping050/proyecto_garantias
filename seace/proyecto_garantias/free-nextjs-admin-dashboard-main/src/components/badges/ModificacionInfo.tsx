"use client";
import React from "react";

interface ModificacionInfoProps {
    usuario?: string;
    fecha?: string;
    usuarioCreacion?: string;
    fechaCreacion?: string;
}

export function ModificacionInfo({
    usuario,
    fecha,
    usuarioCreacion,
    fechaCreacion
}: ModificacionInfoProps) {
    // Si no hay información de modificación, no mostrar nada
    if (!usuario && !usuarioCreacion) {
        return null;
    }

    const formatDate = (dateString: string | undefined) => {
        if (!dateString) return '';
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) return '';
            return date.toLocaleDateString('es-PE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return '';
        }
    };

    return (
        <div className="mt-3 p-3 rounded-lg bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 border border-gray-200 dark:border-gray-700">
            <div className="space-y-2">
                {/* Información de creación (solo para MANUAL) */}
                {usuarioCreacion && (
                    <div className="flex items-start gap-2">
                        <svg className="h-4 w-4 text-emerald-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        <div className="flex-1 min-w-0">
                            <p className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                Creado manualmente
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                                Por <span className="font-semibold">{usuarioCreacion}</span>
                                {fechaCreacion && ` el ${formatDate(fechaCreacion)}`}
                            </p>
                        </div>
                    </div>
                )}

                {/* Información de modificación */}
                {usuario && usuario !== usuarioCreacion && (
                    <div className="flex items-start gap-2">
                        <svg className="h-4 w-4 text-amber-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        <div className="flex-1 min-w-0">
                            <p className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                Última modificación
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                                Por <span className="font-semibold">{usuario}</span>
                                {fecha && ` el ${formatDate(fecha)}`}
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
