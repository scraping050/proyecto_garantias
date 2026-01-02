"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { formatEntityName } from "@/lib/formatUtils";
import { exportLicitacionToPDF } from "@/lib/exportUtils";
import type { Licitacion } from "@/types/licitacion";
import { OrigenBadge } from "@/components/badges/OrigenBadge";
import { ModificacionInfo } from "@/components/badges/ModificacionInfo";

interface LicitacionCardProps {
    licitacion: Licitacion;
    isSelected?: boolean;
    onToggleSelect?: (id: number) => void;
    showDownload?: boolean;
    showMenu?: boolean;
    onEdit?: (licitacion: Licitacion) => void;
    onDelete?: (licitacion: Licitacion) => void;
    onDuplicate?: (licitacion: Licitacion) => void;
    className?: string;
    id?: string;
}

export const LicitacionCard: React.FC<LicitacionCardProps> = ({
    licitacion,
    isSelected,
    onToggleSelect,
    showDownload = true,
    showMenu = false,
    onEdit,
    onDelete,
    onDuplicate,
    className = "",
    id,
}) => {
    const router = useRouter();
    const [isDownloading, setIsDownloading] = useState(false);

    const handleVerDetalles = () => {
        router.push(`/licitaciones/${licitacion.id_convocatoria}`);
    };

    const handleDescargar = async () => {
        try {
            setIsDownloading(true);
            // Use client-side PDF generation for better filename and real PDF format
            exportLicitacionToPDF(licitacion);
        } catch (error) {
            console.error('Error al descargar:', error);
            alert('Error al generar el PDF. Por favor, intente nuevamente.');
        } finally {
            setIsDownloading(false);
        }
    };

    const formatCurrency = (amount: number | null | undefined) => {
        if (!amount || amount === 0) {
            return 'No especificado';
        }
        return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2
        }).format(amount);
    };

    const formatDate = (dateString: string | null | undefined) => {
        if (!dateString) {
            return 'No especificado';
        }
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                return 'Fecha inválida';
            }
            return date.toLocaleDateString('es-PE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        } catch {
            return 'Fecha inválida';
        }
    };

    const getEstadoBadgeColor = (estado: string) => {
        const estadoUpper = estado.toUpperCase();
        if (estadoUpper.includes('ADJUDICADO') || estadoUpper.includes('VIGENTE')) {
            return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
        }
        if (estadoUpper.includes('CONVOCADO') || estadoUpper.includes('PENDIENTE')) {
            return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
        }
        if (estadoUpper.includes('CANCELADO') || estadoUpper.includes('DESIERTO')) {
            return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
        }
        if (estadoUpper.includes('FINALIZADO') || estadoUpper.includes('COMPLETADO')) {
            return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
        }
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400';
    };

    const getCategoriaColor = (categoria: string) => {
        const catUpper = (categoria || "").toUpperCase();
        if (catUpper.includes('BIEN')) return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400';
        if (catUpper.includes('SERVICIO')) return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
        if (catUpper.includes('OBRA')) return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400';
        if (catUpper.includes('CONSULTOR')) return 'bg-teal-100 text-teal-800 dark:bg-teal-900/30 dark:text-teal-400';
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400';
    };

    return (
        <div
            id={id}
            className={`group relative flex flex-col overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-300 hover:shadow-xl hover:border-indigo-300 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-indigo-700 min-h-fit sm:min-h-[600px] ${isSelected ? 'ring-2 ring-indigo-500 bg-indigo-50/10' : ''
                } ${className}`}
        >
            {/* Selection Checkbox */}
            {onToggleSelect && (
                <div className="absolute top-4 right-4 z-20">
                    <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => onToggleSelect(licitacion.id_convocatoria)}
                        onClick={(e) => e.stopPropagation()}
                        className="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer shadow-sm"
                    />
                </div>
            )}

            {/* Content Container */}
            <div className="flex-1 flex flex-col p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-100 dark:bg-indigo-900/30">
                            <svg className="h-6 w-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                                {licitacion.nomenclatura || `ID: ${licitacion.id_convocatoria}`}
                            </h3>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                {licitacion.ocid || `Convocatoria #${licitacion.id_convocatoria}`}
                            </p>
                        </div>
                    </div>
                    <div className="flex flex-col gap-2 items-end">

                        <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${getEstadoBadgeColor(licitacion.estado_proceso)}`}>
                            {licitacion.estado_proceso}
                        </span>
                    </div>
                </div>

                {/* Descripción */}
                <div className="mb-4">
                    <h4 className="text-base font-bold text-gray-900 dark:text-white line-clamp-3">
                        {licitacion.descripcion}
                    </h4>
                </div>

                {/* Details Grid */}
                <div className="space-y-3 mb-4 flex-1">
                    {/* Comprador */}
                    <div className="flex items-start gap-2">
                        <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                        <div className="flex-1 min-w-0">
                            <p className="text-xs text-gray-500 dark:text-gray-400">Comprador</p>
                            <p className="text-sm font-medium text-gray-900 dark:text-white line-clamp-2" title={licitacion.comprador}>
                                {licitacion.comprador}
                            </p>
                        </div>
                    </div>

                    {/* Ubicación */}
                    <div className="flex items-start gap-2">
                        <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <div className="flex-1 min-w-0">
                            <p className="text-xs text-gray-500 dark:text-gray-400">Ubicación</p>
                            <p className="text-sm font-medium text-gray-900 dark:text-white line-clamp-2">
                                {licitacion.departamento}
                                {licitacion.provincia && ` - ${licitacion.provincia}`}
                                {licitacion.distrito && ` - ${licitacion.distrito}`}
                            </p>
                        </div>
                    </div>

                    {/* Categoría */}
                    <div className="flex items-start gap-2">
                        <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                        </svg>
                        <div className="flex-1">
                            <p className="text-xs text-gray-500 dark:text-gray-400">Categoría</p>
                            <div className="flex flex-wrap gap-2 mt-1">
                                <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${getCategoriaColor(licitacion.categoria)}`}>
                                    {licitacion.categoria}
                                </span>
                                {licitacion.tipo_procedimiento && (
                                    <span className="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300">
                                        {licitacion.tipo_procedimiento}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Monto */}
                    <div className="flex items-start gap-2">
                        <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div className="flex-1">
                            {licitacion.monto_total_adjudicado && licitacion.monto_total_adjudicado > 0 ? (
                                <>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">Monto Adjudicado</p>
                                    <p className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                                        {formatCurrency(licitacion.monto_total_adjudicado)}
                                    </p>
                                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                        Estimado: {formatCurrency(licitacion.monto_estimado)}
                                    </p>
                                </>
                            ) : (
                                <>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">Monto Estimado</p>
                                    <p className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                                        {formatCurrency(licitacion.monto_estimado)}
                                    </p>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Fecha */}
                    <div className="flex items-start gap-2">
                        <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <div className="flex-1">
                            {licitacion.fecha_adjudicacion ? (
                                <>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">Fecha de Adjudicación</p>
                                    <p className="text-sm font-medium text-emerald-700 dark:text-emerald-400">
                                        {formatDate(licitacion.fecha_adjudicacion)}
                                    </p>
                                </>
                            ) : (
                                <>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">Fecha de Publicación</p>
                                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                                        {formatDate(licitacion.fecha_publicacion)}
                                    </p>
                                </>
                            )}
                        </div>
                    </div>

                    {/* IDs */}
                    <div className="flex items-start gap-2">
                        <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                        </svg>
                        <div className="flex-1">
                            <p className="text-xs text-gray-500 dark:text-gray-400">Identificadores</p>
                            {licitacion.contratos && licitacion.contratos !== 'null' ? (
                                <>
                                    <p className="text-sm font-mono font-semibold text-indigo-600 dark:text-indigo-400">
                                        ID Contrato: {licitacion.contratos}
                                    </p>
                                    <p className="text-xs font-mono text-gray-600 dark:text-gray-400 mt-1">
                                        ID Convocatoria: {licitacion.id_convocatoria}
                                    </p>
                                </>
                            ) : (
                                <p className="text-sm font-mono font-semibold text-indigo-600 dark:text-indigo-400">
                                    ID Convocatoria: {licitacion.id_convocatoria}
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Ganadores */}
                    {licitacion.ganadores && licitacion.ganadores !== 'null' && (
                        <div className="flex items-start gap-2">
                            <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            <div className="flex-1">
                                <p className="text-xs text-gray-500 dark:text-gray-400">Ganador</p>
                                <p className="text-sm font-medium text-gray-900 dark:text-white">
                                    {licitacion.ganadores}
                                </p>
                                {licitacion.ganadores_ruc && licitacion.ganadores_ruc !== 'null' && (
                                    <p className="text-xs font-mono text-gray-600 dark:text-gray-400 mt-1">
                                        RUC Ganador: {licitacion.ganadores_ruc}
                                    </p>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Tipo de Garantía */}
                    {licitacion.tipos_garantia && licitacion.tipos_garantia !== 'null' && (
                        <div className="flex items-start gap-2">
                            <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                            <div className="flex-1">
                                <p className="text-xs text-gray-500 dark:text-gray-400">Tipo de Garantía</p>
                                <div className="flex flex-wrap gap-2 mt-1">
                                    {licitacion.tipos_garantia.split(', ').map((tipo, idx) => (
                                        <span
                                            key={idx}
                                            className={`inline-flex items-center rounded-md px-2.5 py-1 text-xs font-semibold ${tipo === 'GARANTIA_BANCARIA'
                                                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400'
                                                : tipo === 'RETENCION'
                                                    ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400'
                                                    : 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
                                                }`}
                                        >
                                            {tipo === 'GARANTIA_BANCARIA' ? '🏦 Bancaria' : tipo === 'RETENCION' ? '💰 Retención' : tipo}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Adjudicaciones */}
                    {(licitacion.total_adjudicaciones || licitacion.con_garantia_bancaria) && (
                        <div className="flex items-start gap-2">
                            <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                            <div className="flex-1">
                                <p className="text-xs text-gray-500 dark:text-gray-400">Adjudicaciones</p>
                                <div className="flex flex-wrap gap-2 mt-1 text-xs">
                                    {licitacion.total_adjudicaciones && (
                                        <span className="text-gray-700 dark:text-gray-300">
                                            {licitacion.total_adjudicaciones} item(s)
                                        </span>
                                    )}
                                    {licitacion.con_garantia_bancaria && licitacion.con_garantia_bancaria > 0 && (
                                        <span className="inline-flex items-center gap-1 text-green-700 dark:text-green-400 font-medium">
                                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                            Con Garantía
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Entidades Financieras */}
                    {licitacion.entidades_financieras && licitacion.entidades_financieras !== 'SIN_GARANTIA' && (
                        <div className="flex items-start gap-2">
                            <svg className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                            <div className="flex-1">
                                <p className="text-xs text-gray-500 dark:text-gray-400">Entidades Financieras</p>
                                <div className="mt-1 flex flex-wrap gap-2">
                                    {formatEntityName(licitacion.entidades_financieras).split(',').map((entidad, idx) => (
                                        <span key={idx} className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100 text-xs font-medium text-gray-700 dark:bg-gray-800 dark:text-gray-300 border border-gray-200 dark:border-gray-700">
                                            {entidad.trim()}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Información de Modificación */}
                    <ModificacionInfo
                        usuario={licitacion.usuario_modificacion}
                        fecha={licitacion.fecha_modificacion}
                        usuarioCreacion={licitacion.usuario_creacion}
                        fechaCreacion={licitacion.fecha_creacion}
                    />
                </div>
            </div>

            {/* Actions - always at bottom */}
            <div className="flex flex-col gap-2 p-6 pt-0 border-t border-gray-200 dark:border-gray-800 sm:flex-row">
                <button
                    onClick={handleVerDetalles}
                    className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors dark:bg-indigo-500 dark:hover:bg-indigo-600"
                >
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    <span className="hidden sm:inline">Ver Detalles</span>
                    <span className="sm:hidden">Ver</span>
                </button>

                {/* Edit Button - Only show if onEdit is provided */}
                {showMenu && onEdit && (
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onEdit(licitacion);
                        }}
                        className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                    >
                        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        <span>Editar</span>
                    </button>
                )}

                {/* Delete Button - Only show if onDelete is provided */}
                {showMenu && onDelete && (
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onDelete(licitacion);
                        }}
                        className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg border border-red-300 bg-white px-4 py-2.5 text-sm font-semibold text-red-600 shadow-sm hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors dark:border-red-700 dark:bg-gray-800 dark:text-red-400 dark:hover:bg-red-900/20"
                    >
                        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        <span>Eliminar</span>
                    </button>
                )}

                {/* Download Button - Only show if showDownload is true */}
                {showDownload && (
                    <button
                        onClick={handleDescargar}
                        disabled={isDownloading}
                        className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 sm:flex-none"
                    >
                        {isDownloading ? (
                            <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        ) : (
                            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        )}
                        <span className="hidden sm:inline">{isDownloading ? 'Descargando...' : 'Descargar'}</span>
                        <span className="sm:hidden">{isDownloading ? '...' : 'PDF'}</span>
                    </button>
                )}
            </div>

            {/* Hover Effect */}
            <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-50 to-purple-50 opacity-0 transition-opacity duration-300 group-hover:opacity-100 dark:from-indigo-950/20 dark:to-purple-950/20"></div>
        </div>
    );
};
