'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useNotifications } from '@/hooks/use-notifications';
import { NotificationFilters } from '@/components/notifications/notification-filters';

export default function NotificationsHistoryPage() {
    const [typeFilter, setTypeFilter] = useState('');
    const [priorityFilter, setPriorityFilter] = useState('');
    const router = useRouter();

    const {
        notifications,
        loading,
        fetchNotifications,
        markAsRead,
        markAllAsRead,
        deleteNotification
    } = useNotifications(0); // 0 = sin auto-refresh

    useEffect(() => {
        // Fetch all notifications (including read ones)
        fetchNotifications(false);
    }, [typeFilter, priorityFilter]);

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'high': return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800';
            case 'medium': return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800';
            case 'low': return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800';
            default: return 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700';
        }
    };

    const getPriorityBadge = (priority: string) => {
        switch (priority) {
            case 'high': return <span className="px-2 py-1 bg-red-500 text-white text-xs rounded-full">🔴 Alta</span>;
            case 'medium': return <span className="px-2 py-1 bg-yellow-500 text-white text-xs rounded-full">🟡 Media</span>;
            case 'low': return <span className="px-2 py-1 bg-blue-500 text-white text-xs rounded-full">🔵 Baja</span>;
            default: return null;
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'licitacion': return '📋';
            case 'carta_fianza': return '💳';
            case 'adjudicacion': return '🏆';
            case 'consorcio': return '🤝';
            case 'reporte': return '📊';
            case 'sistema': return '⚙️';
            default: return '📢';
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleString('es-PE', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const filteredNotifications = notifications.filter(notif => {
        if (typeFilter && notif.type !== typeFilter) return false;
        if (priorityFilter && notif.priority !== priorityFilter) return false;
        return true;
    });

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <div className="bg-white dark:bg-gray-800 border-b dark:border-gray-700 sticky top-0 z-10">
                <div className="max-w-6xl mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Historial de Notificaciones</h1>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                {filteredNotifications.length} notificaciones
                                {filteredNotifications.filter(n => !n.is_read).length > 0 && (
                                    <span className="ml-2 text-blue-600 dark:text-blue-400 font-medium">
                                        ({filteredNotifications.filter(n => !n.is_read).length} sin leer)
                                    </span>
                                )}
                            </p>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={() => router.push('/settings')}
                                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors"
                            >
                                <i className="fas fa-arrow-left mr-2"></i>
                                Volver
                            </button>
                            {filteredNotifications.some(n => !n.is_read) && (
                                <button
                                    onClick={markAllAsRead}
                                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                                >
                                    <i className="fas fa-check-double mr-2"></i>
                                    Marcar todas leídas
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div className="max-w-6xl mx-auto px-6 py-4">
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
                    <NotificationFilters
                        typeFilter={typeFilter}
                        priorityFilter={priorityFilter}
                        onChange={(f) => {
                            setTypeFilter(f.type);
                            setPriorityFilter(f.priority);
                        }}
                    />
                </div>
            </div>

            {/* Notifications List */}
            <div className="max-w-6xl mx-auto px-6 pb-8">
                {loading ? (
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
                        <i className="fas fa-circle-notch fa-spin text-4xl text-blue-500 mb-4"></i>
                        <p className="text-gray-600 dark:text-gray-400">Cargando notificaciones...</p>
                    </div>
                ) : filteredNotifications.length === 0 ? (
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-12 text-center">
                        <i className="fas fa-bell-slash text-6xl text-gray-300 dark:text-gray-600 mb-4"></i>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No hay notificaciones</h3>
                        <p className="text-gray-600 dark:text-gray-400">
                            {typeFilter || priorityFilter
                                ? 'No se encontraron notificaciones con los filtros seleccionados'
                                : 'Estás al día con todas las notificaciones'
                            }
                        </p>
                    </div>
                ) : (
                    <div className="space-y-3">
                        {filteredNotifications.map((notif) => (
                            <div
                                key={notif.id}
                                className={`bg-white dark:bg-gray-800 rounded-lg shadow-sm border-2 transition-all hover:shadow-md ${!notif.is_read ? 'border-blue-300 dark:border-blue-700 bg-blue-50/30 dark:bg-blue-900/10' : 'border-gray-200 dark:border-gray-700'
                                    } ${getPriorityColor(notif.priority)}`}
                            >
                                <div className="p-5">
                                    <div className="flex items-start gap-4">
                                        {/* Icon */}
                                        <div className="text-4xl flex-shrink-0">
                                            {getTypeIcon(notif.type)}
                                        </div>

                                        {/* Content */}
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-start justify-between gap-4 mb-2">
                                                <div className="flex-1">
                                                    <h3 className="font-bold text-gray-900 dark:text-white text-lg mb-1">
                                                        {notif.title}
                                                        {!notif.is_read && (
                                                            <span className="ml-2 inline-block w-2 h-2 bg-blue-500 rounded-full"></span>
                                                        )}
                                                    </h3>
                                                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{notif.message}</p>
                                                </div>
                                                {getPriorityBadge(notif.priority)}
                                            </div>

                                            {/* Meta */}
                                            <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mt-3">
                                                <span>
                                                    <i className="fas fa-clock mr-1"></i>
                                                    {formatDate(notif.created_at)}
                                                </span>
                                                {notif.link && (
                                                    <button
                                                        onClick={() => router.push(notif.link!)}
                                                        className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium"
                                                    >
                                                        <i className="fas fa-external-link-alt mr-1"></i>
                                                        Ver detalles
                                                    </button>
                                                )}
                                            </div>
                                        </div>

                                        {/* Actions */}
                                        <div className="flex flex-col gap-2 flex-shrink-0">
                                            {!notif.is_read && (
                                                <button
                                                    onClick={() => markAsRead(notif.id)}
                                                    className="px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm"
                                                    title="Marcar como leída"
                                                >
                                                    <i className="fas fa-check"></i>
                                                </button>
                                            )}
                                            <button
                                                onClick={() => deleteNotification(notif.id)}
                                                className="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
                                                title="Eliminar"
                                            >
                                                <i className="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
