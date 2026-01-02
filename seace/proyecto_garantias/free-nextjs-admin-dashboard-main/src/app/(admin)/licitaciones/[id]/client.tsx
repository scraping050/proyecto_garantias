"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import type { Licitacion } from "@/types/licitacion";

interface LicitacionDetalle {
    licitacion: Licitacion;
    adjudicaciones: any[];
    contratos: any[];
    consorcios: any[];
    resumen: {
        total_adjudicaciones: number;
        total_contratos: number;
        monto_total_adjudicado: number;
        con_garantia_bancaria: number;
    };
}

export default function LicitacionClient({ id }: { id: string }) {
    const router = useRouter();
    // const resolvedParams = React.use(params); // Removed, using id prop directly
    const [data, setData] = useState<LicitacionDetalle | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                // Use id (from prop) instead of resolvedParams.id
                // Also update URL to use production API if needed? No, localhost:5000 is in original code.
                // Wait, original code had fetch('http://localhost:5000/api/...') in Step 531 line 30.
                // This will FAIL in production (client side request to localhost).
                // I should fix this to use env var!
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';
                const response = await fetch(`${apiUrl}/licitaciones/${id}`);

                if (!response.ok) {
                    throw new Error('Licitación no encontrada');
                }

                const result = await response.json();
                setData(result.data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Error al cargar los datos');
            } finally {
                setLoading(false);
            }
        };

        if (id) {
            fetchData();
        }
    }, [id]);

    const formatCurrency = (amount: number | null | undefined) => {
        if (!amount || amount === 0) return 'No especificado';
        return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2
        }).format(amount);
    };

    const formatDate = (dateString: string | null | undefined) => {
        if (!dateString) return 'No especificado';
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) return 'Fecha inválida';
            return date.toLocaleDateString('es-PE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        } catch {
            return 'Fecha inválida';
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando detalles...</p>
                </div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <svg className="h-16 w-16 text-red-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h2 className="mt-4 text-xl font-semibold text-gray-900 dark:text-white">Error</h2>
                    <p className="mt-2 text-gray-600 dark:text-gray-400">{error}</p>
                    <button
                        onClick={() => router.back()}
                        className="mt-4 inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
                    >
                        Volver
                    </button>
                </div>
            </div>
        );
    }

    const { licitacion, adjudicaciones, contratos, consorcios, resumen } = data;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <button
                    onClick={() => router.back()}
                    className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
                >
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver a resultados
                </button>
            </div>

            {/* Main Info Card */}
            <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm dark:border-gray-800 dark:bg-gray-900">
                <div className="flex flex-col md:flex-row md:items-start justify-between mb-8 gap-4">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                                Licitación #{licitacion.id_convocatoria}
                            </h1>
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${licitacion.estado_proceso === 'ADJUDICADO' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                                {licitacion.estado_proceso}
                            </span>
                        </div>
                        <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                            {licitacion.descripcion}
                        </p>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                        <div className="text-right">
                            <p className="text-sm text-gray-500 dark:text-gray-400">Monto Estimado</p>
                            <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                                {formatCurrency(licitacion.monto_estimado)}
                            </p>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-8 border-t border-gray-100 dark:border-gray-800">
                    <div className="space-y-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                            Entidad Convocante
                        </h3>
                        <div>
                            <p className="font-medium text-gray-900 dark:text-white">{licitacion.comprador}</p>
                            <p className="text-sm text-gray-500 dark:text-gray-400">{licitacion.departamento} - {licitacion.provincia}</p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                            Detalles del Proceso
                        </h3>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <p className="text-gray-500 dark:text-gray-400">Nomenclatura</p>
                                <p className="font-medium text-gray-900 dark:text-white">{licitacion.nomenclatura}</p>
                            </div>
                            <div>
                                <p className="text-gray-500 dark:text-gray-400">Categoría</p>
                                <p className="font-medium text-gray-900 dark:text-white">{licitacion.categoria}</p>
                            </div>
                            <div>
                                <p className="text-gray-500 dark:text-gray-400">Fecha Publicación</p>
                                <p className="font-medium text-gray-900 dark:text-white">{formatDate(licitacion.fecha_publicacion)}</p>
                            </div>
                            <div>
                                <p className="text-gray-500 dark:text-gray-400">OCID</p>
                                <p className="font-mono text-gray-900 dark:text-white">{licitacion.ocid}</p>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" />
                            </svg>
                            Resumen Financiero
                        </h3>
                        <div className="space-y-2">
                            <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                                <span className="text-sm text-gray-600 dark:text-gray-300">Total Adjudicado</span>
                                <span className="font-bold text-indigo-600 dark:text-indigo-400">{formatCurrency(resumen.monto_total_adjudicado)}</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-500">Contratos</span>
                                <span className="font-medium dark:text-white">{resumen.total_contratos}</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-500">Garantías Bancarias</span>
                                <span className={`font-medium ${resumen.con_garantia_bancaria > 0 ? 'text-green-600' : 'text-gray-900 dark:text-white'}`}>
                                    {resumen.con_garantia_bancaria}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Consorcios Section */}
            {consorcios && consorcios.length > 0 && (
                <div className="rounded-2xl border border-indigo-100 bg-indigo-50/50 p-6 dark:border-indigo-900/30 dark:bg-indigo-950/20">
                    <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                        <svg className="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        Detalle de Miembros del Consorcio
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {consorcios.map((miembro: any, idx: number) => (
                            <div key={idx} className="bg-white p-4 rounded-xl border border-indigo-100 shadow-sm dark:bg-gray-800 dark:border-gray-700">
                                <div className="flex justify-between items-start mb-2">
                                    <div className="bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-1 rounded dark:bg-indigo-900 dark:text-indigo-300">
                                        {miembro.porcentaje_participacion}%
                                    </div>
                                    <span className="text-xs text-gray-400 font-mono">{miembro.ruc_miembro}</span>
                                </div>
                                <h4 className="font-semibold text-gray-900 dark:text-white text-sm line-clamp-2 mb-3" title={miembro.nombre_miembro}>
                                    {miembro.nombre_miembro}
                                </h4>
                                <div className="w-full bg-gray-200 rounded-full h-1.5 dark:bg-gray-700">
                                    <div
                                        className="bg-indigo-600 h-1.5 rounded-full transition-all duration-500"
                                        style={{ width: `${miembro.porcentaje_participacion}%` }}
                                    ></div>
                                </div>
                                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                                    Consorcio: {miembro.consorcio_padre}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Adjudicaciones Detail */}
            {adjudicaciones.length > 0 && (
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
                    <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                        Detalle de Adjudicaciones
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
                            <thead>
                                <tr className="bg-gray-50 dark:bg-gray-800/50">
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Ganador / Proveedor</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Monto</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Garantía</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Entidad Financiera</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Estado</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                                {adjudicaciones.map((adj: any, index: number) => (
                                    <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                                        <td className="px-4 py-4">
                                            <p className="text-sm font-medium text-gray-900 dark:text-white">{adj.ganador_nombre}</p>
                                            <p className="text-xs text-gray-500 font-mono mt-0.5">{adj.ganador_ruc}</p>
                                        </td>
                                        <td className="px-4 py-4 text-sm font-semibold text-gray-900 dark:text-white">
                                            {formatCurrency(adj.monto_adjudicado)}
                                        </td>
                                        <td className="px-4 py-4">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                                                ${adj.tipo_garantia === 'GARANTIA_BANCARIA'
                                                    ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400'
                                                    : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'}`}>
                                                {adj.tipo_garantia || 'N/A'}
                                            </span>
                                        </td>
                                        <td className="px-4 py-4 text-sm text-gray-600 dark:text-gray-300">
                                            {adj.entidad_financiera && adj.entidad_financiera !== 'SIN_GARANTIA' ? (
                                                <div className="flex items-center gap-2">
                                                    <svg className="w-4 h-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                                                    </svg>
                                                    {adj.entidad_financiera}
                                                </div>
                                            ) : (
                                                <span className="text-gray-400 italic">No registrada</span>
                                            )}
                                        </td>
                                        <td className="px-4 py-4">
                                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                                {formatDate(adj.fecha_adjudicacion)}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
