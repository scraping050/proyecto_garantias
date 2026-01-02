"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";

interface NotificationBellProps {
    className?: string;
}

export const NotificationBell: React.FC<NotificationBellProps> = ({ className = "" }) => {
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);
    const [notifications, setNotifications] = useState<any[]>([]);

    // Fetch unread count
    const fetchUnreadCount = async () => {
        try {
            const response = await fetch("/api/notificaciones/count");
            const data = await response.json();
            if (data.success) {
                setUnreadCount(data.count);
            }
        } catch (error) {
            console.error("Error fetching notification count:", error);
        }
    };

    // Fetch recent notifications
    const fetchRecentNotifications = async () => {
        try {
            const response = await fetch("/api/notificaciones?page=1&per_page=5");
            const data = await response.json();
            if (data.success) {
                setNotifications(data.data);
            }
        } catch (error) {
            console.error("Error fetching notifications:", error);
        }
    };

    useEffect(() => {
        fetchUnreadCount();
        // Refresh every 5 seconds for near real-time updates
        const interval = setInterval(fetchUnreadCount, 5000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (isOpen) {
            fetchRecentNotifications();
        }
    }, [isOpen]);

    const handleMarkAsRead = async (id: number) => {
        try {
            await fetch(`/api/notificaciones/${id}/read`, {
                method: "PUT",
            });
            fetchUnreadCount();
            fetchRecentNotifications();
        } catch (error) {
            console.error("Error marking notification as read:", error);
        }
    };

    const formatTimeAgo = (dateString: string) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return "Ahora";
        if (diffMins < 60) return `Hace ${diffMins} min`;
        if (diffHours < 24) return `Hace ${diffHours}h`;
        return `Hace ${diffDays}d`;
    };

    return (
        <div className={`relative ${className}`}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="relative flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
                <svg
                    className="w-6 h-6 text-gray-600 dark:text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                </svg>
                {unreadCount > 0 && (
                    <span className="absolute top-0 right-0 flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full">
                        {unreadCount > 99 ? "99+" : unreadCount}
                    </span>
                )}
            </button>

            {isOpen && (
                <>
                    <div
                        className="fixed inset-0 z-40"
                        onClick={() => setIsOpen(false)}
                    />
                    <div className="absolute right-0 z-50 mt-2 w-80 bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
                        <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-800">
                            <div className="flex items-center justify-between">
                                <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                                    Notificaciones
                                </h3>
                                {unreadCount > 0 && (
                                    <span className="text-xs text-gray-500 dark:text-gray-400">
                                        {unreadCount} nueva{unreadCount !== 1 ? "s" : ""}
                                    </span>
                                )}
                            </div>
                        </div>

                        <div className="max-h-96 overflow-y-auto">
                            {notifications.length === 0 ? (
                                <div className="px-4 py-8 text-center">
                                    <svg
                                        className="w-12 h-12 mx-auto text-gray-400 mb-2"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                                        />
                                    </svg>
                                    <p className="text-sm text-gray-500 dark:text-gray-400">
                                        No hay notificaciones
                                    </p>
                                </div>
                            ) : (
                                notifications.map((notification) => (
                                    <div
                                        key={notification.id}
                                        className={`px-4 py-3 border-b border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors ${!notification.leida ? "bg-blue-50/50 dark:bg-blue-900/10" : ""
                                            }`}
                                    >
                                        <div className="flex items-start gap-3">
                                            <div className="flex-shrink-0 mt-1">
                                                <div className={`w-2 h-2 rounded-full ${!notification.leida ? "bg-blue-500" : "bg-gray-300"}`} />
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <div className="flex justify-between items-start gap-2">
                                                    <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                                        Cambio de Estado: <span className="text-blue-600">{notification.ocid || notification.id_convocatoria || "S/N"}</span>
                                                    </p>
                                                    {!notification.leida && (
                                                        <button
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                handleMarkAsRead(notification.id);
                                                            }}
                                                            className="flex-shrink-0 text-xs text-blue-600 hover:text-blue-700 dark:text-blue-400 whitespace-nowrap"
                                                        >
                                                            Marcar
                                                        </button>
                                                    )}
                                                </div>

                                                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                                    {notification.estado_anterior} → <span className={`font-medium ${notification.estado_nuevo === 'ADJUDICADO' ? 'text-green-600' :
                                                        notification.estado_nuevo === 'NULO' ? 'text-red-600' :
                                                            notification.estado_nuevo === 'DESIERTO' ? 'text-orange-600' : 'text-gray-700'
                                                        }`}>{notification.estado_nuevo}</span>
                                                </p>

                                                <div className="flex justify-between items-center mt-2">
                                                    <p className="text-xs text-gray-400 dark:text-gray-500">
                                                        {formatTimeAgo(notification.fecha_creacion)}
                                                    </p>
                                                    <Link
                                                        href={`/notificaciones?highlight=${notification.id}`}
                                                        onClick={() => setIsOpen(false)}
                                                        className="text-xs font-semibold text-blue-600 hover:text-blue-800 hover:underline dark:text-blue-400"
                                                    >
                                                        Ver
                                                    </Link>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>

                        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
                            <Link
                                href="/notificaciones"
                                className="block text-center text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400"
                                onClick={() => setIsOpen(false)}
                            >
                                Ver todas las notificaciones
                            </Link>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};
