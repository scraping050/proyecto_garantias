"use client";
import React, { useState, useEffect } from "react";
import type { Notification, NotificationsResponse } from "@/types/notification";
import Link from "next/link";
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import Badge from "@/components/ui/badge/Badge";

import { useSearchParams } from "next/navigation";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

function NotificacionesContent() {
    const searchParams = useSearchParams();
    const highlightId = searchParams.get("highlight");
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<"all" | "unread" | "read">("all");
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const perPage = 10; // Reduced for table view


    // Mock Data for Design Preview
    const mockNotifications: Notification[] = [
        {
            id: 99901,
            id_convocatoria: "2024-C-001",
            tipo: "CAMBIO_ESTADO",
            titulo: "Licitación Adjudicada en Cusco",
            mensaje: "El proceso para 'Mejoramiento de vías en San Jerónimo' ha cambiado de estado.",
            estado_anterior: "CONVOCADO",
            estado_nuevo: "ADJUDICADO",
            leida: false,
            fecha_creacion: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
            fecha_lectura: null,
            metadata: { departamento: "CUSCO", monto_estimado: 1250000.50, categoria: "OBRAS" }
        },
        {
            id: 99902,
            id_convocatoria: "2024-S-055",
            tipo: "CAMBIO_ESTADO",
            titulo: "Proceso Desierto en Lima",
            mensaje: "No se presentaron postores válidos para el servicio de vigilancia.",
            estado_anterior: "CONVOCADO",
            estado_nuevo: "DESIERTO",
            leida: false,
            fecha_creacion: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5 hours ago
            fecha_lectura: null,
            metadata: { departamento: "LIMA", monto_estimado: 45000.00, categoria: "SERVICIOS" }
        },
        {
            id: 99903,
            id_convocatoria: "2024-B-777",
            tipo: "CAMBIO_ESTADO",
            titulo: "Contrato Firmado - Piura",
            mensaje: "Se ha perfeccionado el contrato para la adquisición de mobiliario escolar.",
            estado_anterior: "ADJUDICADO",
            estado_nuevo: "CONTRATADO",
            leida: true,
            fecha_creacion: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
            fecha_lectura: new Date().toISOString(),
            metadata: { departamento: "PIURA", monto_estimado: 89000.00, categoria: "BIENES" }
        },
        {
            id: 99904,
            id_convocatoria: "2024-O-999",
            tipo: "CAMBIO_ESTADO",
            titulo: "Proceso NULO por Vicios",
            mensaje: "Se declaró la nulidad de oficio del proceso de construcción de puente.",
            estado_anterior: "ADJUDICADO",
            estado_nuevo: "NULO",
            leida: false,
            fecha_creacion: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(), // 2 days ago
            fecha_lectura: null,
            metadata: { departamento: "AREQUIPA", monto_estimado: 5400000.00, categoria: "OBRAS" }
        }
    ];

    const fetchNotifications = async () => {
        try {
            setLoading(true);
            const leidaParam = filter === "all" ? "" : `&leida=${filter === "read"}`;
            const response = await fetch(
                `${API_BASE_URL}/api/notificaciones?page=${currentPage}&per_page=${perPage}${leidaParam}`
            );
            const data: NotificationsResponse = await response.json();

            if (data.success) {
                // Use real data only
                setNotifications(data.data);
                setTotalPages(data.pagination.total_pages || 1);
            }
        } catch (error) {
            console.error("Error fetching notifications:", error);
            setNotifications([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNotifications();
    }, [currentPage, filter]);

    // Handle highlighting after notifications load
    useEffect(() => {
        if (highlightId && notifications.length > 0) {
            const element = document.getElementById(`notification-${highlightId}`);
            if (element) {
                element.scrollIntoView({ behavior: "smooth", block: "center" });
                // Add temporary flash effect
                element.classList.add("bg-blue-50", "dark:bg-blue-900/20", "ring-2", "ring-blue-500");
                setTimeout(() => {
                    element.classList.remove("bg-blue-50", "dark:bg-blue-900/20", "ring-2", "ring-blue-500");
                }, 3000);
            }
        }
    }, [highlightId, notifications]);

    const handleMarkAsRead = async (id: number) => {
        try {
            await fetch(`${API_BASE_URL}/api/notificaciones/${id}/read`, {
                method: "PUT",
            });
            fetchNotifications();
        } catch (error) {
            console.error("Error marking notification as read:", error);
        }
    };

    const handleMarkAllAsRead = async () => {
        try {
            await fetch(`${API_BASE_URL}/api/notificaciones/read-all`, {
                method: "PUT",
            });
            fetchNotifications();
        } catch (error) {
            console.error("Error marking all as read:", error);
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm("¿Estás seguro de eliminar esta notificación?")) return;

        try {
            await fetch(`${API_BASE_URL}/api/notificaciones/${id}`, {
                method: "DELETE",
            });
            fetchNotifications();
        } catch (error) {
            console.error("Error deleting notification:", error);
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat("es-PE", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        }).format(date);
    };

    // Helper for Badge colors based on status
    const getBadgeColor = (estado: string | null) => {
        if (!estado) return "light";
        const e = estado.toUpperCase();
        if (e.includes("CONTR")) return "success";
        if (e.includes("ADJUD")) return "success";
        if (e.includes("DESIE") || e.includes("NULO") || e.includes("CANCEL")) return "error";
        if (e.includes("CONVO")) return "info";
        return "warning";
    };

    return (
        <div className="space-y-6">
            {/* Header & Controls */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                        Notificaciones
                    </h1>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        Historial de cambios en licitaciones
                    </p>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={handleMarkAllAsRead}
                        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none dark:focus:ring-offset-gray-900"
                    >
                        Marcar todas leídas
                    </button>
                </div>
            </div>

            {/* Filters */}
            <div className="flex gap-2">
                {(["all", "unread", "read"] as const).map((f) => (
                    <button
                        key={f}
                        onClick={() => { setFilter(f); setCurrentPage(1); }}
                        className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${filter === f
                            ? "bg-blue-600 text-white"
                            : "bg-white text-gray-700 hover:bg-gray-50 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800"
                            }`}
                    >
                        {f === "all" ? "Todas" : f === "unread" ? "No leídas" : "Leídas"}
                    </button>
                ))}
            </div>

            {/* Table Container (Based on BasicTableOne style) */}
            <div className="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-white/[0.05] dark:bg-white/[0.03]">
                <div className="max-w-full overflow-x-auto">
                    <div className="min-w-[1000px]">
                        <Table>
                            <TableHeader className="border-b border-gray-100 dark:border-white/[0.05]">
                                <TableRow>
                                    <TableCell isHeader className="px-5 py-4 font-semibold text-gray-500 text-start text-sm dark:text-gray-400 w-[40%]">
                                        Licitación
                                    </TableCell>
                                    <TableCell isHeader className="px-5 py-4 font-semibold text-gray-500 text-start text-sm dark:text-gray-400 w-[20%]">
                                        Detalles
                                    </TableCell>
                                    <TableCell isHeader className="px-5 py-4 font-semibold text-gray-500 text-center text-sm dark:text-gray-400 w-[20%]">
                                        Cambio de Estado
                                    </TableCell>
                                    <TableCell isHeader className="px-5 py-4 font-semibold text-gray-500 text-center text-sm dark:text-gray-400 w-[10%]">
                                        Fecha
                                    </TableCell>
                                    <TableCell isHeader className="px-5 py-4 font-semibold text-gray-500 text-center text-sm dark:text-gray-400 w-[10%]">
                                        Acciones
                                    </TableCell>
                                </TableRow>
                            </TableHeader>

                            <TableBody className="divide-y divide-gray-100 dark:divide-white/[0.05]">
                                {loading ? (
                                    // Skeleton Loading Rows
                                    [...Array(5)].map((_, i) => (
                                        <TableRow key={i}>
                                            <TableCell className="px-5 py-4"><div className="h-4 w-48 bg-gray-200 rounded animate-pulse"></div></TableCell>
                                            <TableCell className="px-5 py-4"><div className="h-4 w-32 bg-gray-200 rounded animate-pulse"></div></TableCell>
                                            <TableCell className="px-5 py-4"><div className="h-4 w-24 bg-gray-200 rounded animate-pulse"></div></TableCell>
                                            <TableCell className="px-5 py-4"><div className="h-4 w-20 bg-gray-200 rounded animate-pulse"></div></TableCell>
                                            <TableCell className="px-5 py-4"><div className="h-8 w-8 bg-gray-200 rounded animate-pulse"></div></TableCell>
                                        </TableRow>
                                    ))
                                ) : notifications.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={5}>
                                            <div className="flex flex-col items-center justify-center py-24 text-center w-full max-w-2xl mx-auto">
                                                <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 dark:bg-gray-800">
                                                    <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                                                    </svg>
                                                </div>
                                                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                                                    Sin Notificaciones
                                                </h3>
                                                <p className="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
                                                    Te avisaremos cuando haya cambios importantes en tus licitaciones seguidas o procesos relevantes.
                                                </p>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    notifications.map((notification) => (
                                        <TableRow
                                            key={notification.id}
                                            id={`notification-${notification.id}`}
                                            className="hover:bg-gray-50 dark:hover:bg-white/[0.02] transition-all duration-500 ease-in-out"
                                        >
                                            {/* Column 1: Title & Message (User/Project style) */}
                                            <TableCell className="px-5 py-4 sm:px-6 align-middle">
                                                <div className="flex items-start gap-4">
                                                    {/* Unread Indicator Dot */}
                                                    <div className={`mt-2 w-2.5 h-2.5 rounded-full flex-shrink-0 ${!notification.leida ? 'bg-blue-500 ring-2 ring-blue-100 dark:ring-blue-900' : 'bg-transparent border border-gray-300 dark:border-gray-600'}`} />

                                                    <div>
                                                        <span className={`block text-theme-sm dark:text-white/90 ${!notification.leida ? 'font-semibold text-gray-900' : 'font-medium text-gray-700'}`}>
                                                            {notification.titulo}
                                                        </span>
                                                        <span className="block text-gray-500 text-theme-xs dark:text-gray-400 mt-1 line-clamp-2 max-w-[320px] leading-relaxed">
                                                            {notification.mensaje}
                                                        </span>
                                                        <Link
                                                            href={`/busqueda-licitaciones?id=${notification.id_convocatoria}`}
                                                            className="text-theme-xs text-blue-600 hover:text-blue-700 font-medium mt-2 inline-flex items-center gap-1 group"
                                                        >
                                                            Ver Orcid: {notification.ocid || notification.id_convocatoria}
                                                            <svg className="w-3 h-3 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
                                                        </Link>
                                                    </div>
                                                </div>
                                            </TableCell>

                                            {/* Column 2: Details (Monto, Dept, Categoria) */}
                                            <TableCell className="px-4 py-3 align-middle">
                                                <div className="flex flex-col gap-2">
                                                    {notification.metadata?.categoria && (
                                                        <div className="flex items-center gap-2 text-theme-xs text-gray-600 dark:text-gray-300">
                                                            <div className="p-1 rounded bg-orange-50 text-orange-600 dark:bg-orange-900/20 dark:text-orange-400">
                                                                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
                                                            </div>
                                                            <span className="font-medium">{notification.metadata.categoria}</span>
                                                        </div>
                                                    )}
                                                    {notification.metadata?.departamento && (
                                                        <div className="flex items-center gap-2 text-theme-xs text-gray-500 dark:text-gray-400">
                                                            <div className="p-1 rounded bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400">
                                                                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                                                            </div>
                                                            {notification.metadata.departamento}
                                                        </div>
                                                    )}
                                                    {notification.metadata?.monto_estimado && (
                                                        <div className="flex items-center gap-2 text-theme-xs font-medium text-gray-700 dark:text-gray-300">
                                                            <div className="p-1 rounded bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400">
                                                                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                                            </div>
                                                            S/ {Number(notification.metadata.monto_estimado).toLocaleString()}
                                                        </div>
                                                    )}
                                                </div>
                                            </TableCell>

                                            {/* Column 3: Status Change (Professional Timeline) */}
                                            <TableCell className="px-4 py-3 align-middle text-center">
                                                <div className="flex items-center justify-center gap-3">
                                                    {/* Old Status */}
                                                    {notification.estado_anterior && (
                                                        <div className="opacity-70 grayscale scale-90">
                                                            <Badge size="sm" color="light">
                                                                {notification.estado_anterior}
                                                            </Badge>
                                                        </div>
                                                    )}

                                                    {/* Arrow */}
                                                    {notification.estado_anterior && notification.estado_nuevo && (
                                                        <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                                                        </svg>
                                                    )}

                                                    {/* New Status */}
                                                    <Badge
                                                        size="sm"
                                                        color={getBadgeColor(notification.estado_nuevo)}
                                                    >
                                                        {notification.estado_nuevo || "Desconocido"}
                                                    </Badge>
                                                </div>
                                            </TableCell>

                                            {/* Column 4: Date */}
                                            <TableCell className="px-4 py-3 text-gray-500 text-theme-sm dark:text-gray-400 whitespace-nowrap align-middle">
                                                <div className="flex flex-col items-center justify-center">
                                                    <span className="font-medium text-gray-700 dark:text-gray-300">
                                                        {new Date(notification.fecha_creacion).toLocaleDateString('es-PE', { day: 'numeric', month: 'short', year: 'numeric' })}
                                                    </span>
                                                    <span className="text-xs text-gray-400">
                                                        {new Date(notification.fecha_creacion).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })}
                                                    </span>
                                                </div>
                                            </TableCell>

                                            {/* Column 5: Actions */}
                                            <TableCell className="px-4 py-3 align-middle">
                                                <div className="flex items-center justify-center gap-2">
                                                    {!notification.leida && (
                                                        <button
                                                            onClick={() => handleMarkAsRead(notification.id)}
                                                            className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors dark:text-gray-400 dark:hover:text-blue-400 dark:hover:bg-blue-900/20"
                                                            title="Marcar leído"
                                                        >
                                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                                            </svg>
                                                        </button>
                                                    )}
                                                    <button
                                                        onClick={() => handleDelete(notification.id)}
                                                        className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors dark:text-gray-400 dark:hover:text-red-400 dark:hover:bg-red-900/20"
                                                        title="Eliminar"
                                                    >
                                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                                        </svg>
                                                    </button>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </div>
                </div>
            </div>

            {/* Pagination */}
            {!loading && totalPages > 1 && (
                <div className="flex items-center justify-center gap-2 mt-6">
                    <button
                        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                        disabled={currentPage === 1}
                        className="px-4 py-2 text-sm font-medium bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700"
                    >
                        Anterior
                    </button>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                        Página {currentPage} de {totalPages}
                    </span>
                    <button
                        onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                        disabled={currentPage === totalPages}
                        className="px-4 py-2 text-sm font-medium bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700"
                    >
                        Siguiente
                    </button>
                </div>
            )}
        </div>
    );
}

export default function NotificacionesPage() {
    return (
        <React.Suspense fallback={<div className="p-8">Cargando notificaciones...</div>}>
            <NotificacionesContent />
        </React.Suspense>
    );
}
