```javascript
"use client";
import Link from "next/link";
import React, { useState, useEffect } from "react";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import type { Notification } from "@/types/notification";

export default function NotificationDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  function toggleDropdown() {
    setIsOpen(!isOpen);
    if (!isOpen) {
      fetchNotifications();
    }
  }

  function closeDropdown() {
    setIsOpen(false);
  }

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      // Fetch latest 5 unread or all notifications
      const response = await fetch('http://localhost:5000/api/notificaciones?page=1&per_page=5');
      const data = await response.json();
      if (data.success) {
        setNotifications(data.data);
      }
    } catch (error) {
      console.error("Error fetching notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUnreadCount = async () => {
      try {
          const response = await fetch('http://localhost:5000/api/notificaciones/count');
          const data = await response.json();
          if (data.success) {
              setUnreadCount(data.count);
          }
      } catch (error) {
          console.error("Error fetching count:", error);
      }
  };

  useEffect(() => {
      fetchUnreadCount();
      // Optional: Polling every minute
      const interval = setInterval(fetchUnreadCount, 60000);
      return () => clearInterval(interval);
  }, []);

  const handleMarkAsRead = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    try {
        await fetch(`http://localhost:5000/api/notificaciones/${id}/read`, { method: 'PUT' });
// Update local state
setNotifications(prev => prev.map(n => n.id === id ? { ...n, leida: true } : n));
setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
  console.error("Error marking as read:", error);
}
  };

return (
  <div className="relative">
    <button
      className="relative dropdown-toggle flex items-center justify-center text-gray-500 transition-colors bg-white border border-gray-200 rounded-full hover:text-gray-700 h-11 w-11 hover:bg-gray-100 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-white"
      onClick={toggleDropdown}
    >
      <span
        className={`absolute right-0 top-0.5 z-10 h-2 w-2 rounded-full bg-orange-400 ${unreadCount === 0 ? "hidden" : "flex"
          }`}
      >
        <span className="absolute inline-flex w-full h-full bg-orange-400 rounded-full opacity-75 animate-ping"></span>
      </span>
      <svg
        className="fill-current"
        width="20"
        height="20"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fillRule="evenodd"
          clipRule="evenodd"
          d="M10.75 2.29248C10.75 1.87827 10.4143 1.54248 10 1.54248C9.58583 1.54248 9.25004 1.87827 9.25004 2.29248V2.83613C6.08266 3.20733 3.62504 5.9004 3.62504 9.16748V14.4591H3.33337C2.91916 14.4591 2.58337 14.7949 2.58337 15.2091C2.58337 15.6234 2.91916 15.9591 3.33337 15.9591H4.37504H15.625H16.6667C17.0809 15.9591 17.4167 15.6234 17.4167 15.2091C17.4167 14.7949 17.0809 14.4591 16.6667 14.4591H16.375V9.16748C16.375 5.9004 13.9174 3.20733 10.75 2.83613V2.29248ZM14.875 14.4591V9.16748C14.875 6.47509 12.6924 4.29248 10 4.29248C7.30765 4.29248 5.12504 6.47509 5.12504 9.16748V14.4591H14.875ZM8.00004 17.7085C8.00004 18.1228 8.33583 18.4585 8.75004 18.4585H11.25C11.6643 18.4585 12 18.1228 12 17.7085C12 17.2943 11.6643 16.9585 11.25 16.9585H8.75004C8.33583 16.9585 8.00004 17.2943 8.00004 17.7085Z"
          fill="currentColor"
        />
      </svg>
    </button>
    <Dropdown
      isOpen={isOpen}
      onClose={closeDropdown}
      className="absolute -right-[240px] mt-[17px] flex h-[480px] w-[350px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark sm:w-[361px] lg:right-0"
    >
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-gray-100 dark:border-gray-700">
        <h5 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
          Notificaciones {unreadCount > 0 && `(${unreadCount})`}
        </h5>
        <button
          onClick={toggleDropdown}
          className="text-gray-500 transition dropdown-toggle dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
        >
          <svg className="fill-current" width="24" height="24" viewBox="0 0 24 24"><path fillRule="evenodd" clipRule="evenodd" d="M6.21967 7.28131C5.92678 6.98841 5.92678 6.51354 6.21967 6.22065C6.51256 5.92775 6.98744 5.92775 7.28033 6.22065L11.999 10.9393L16.7176 6.22078C17.0105 5.92789 17.4854 5.92788 17.7782 6.22078C18.0711 6.51367 18.0711 6.98855 17.7782 7.28144L13.0597 12L17.7782 16.7186C18.0711 17.0115 18.0711 17.4863 17.7782 17.7792C17.4854 18.0721 17.0105 18.0721 16.7176 17.7792L11.999 13.0607L7.28033 17.7794C6.98744 18.0722 6.51256 18.0722 6.21967 17.7794C5.92678 17.4865 5.92678 17.0116 6.21967 16.7187L10.9384 12L6.21967 7.28131Z" fill="currentColor" /></svg>
        </button>
      </div>

      <ul className="flex flex-col h-auto overflow-y-auto custom-scrollbar gap-1">
        {loading && <p className="text-center p-4 text-gray-500">Cargando...</p>}
        {!loading && notifications.length === 0 && <p className="text-center p-4 text-gray-500">No hay notificaciones</p>}

        {notifications.map((notification) => (
          <li key={notification.id}>
            <DropdownItem
              onItemClick={() => { }} // Do NOT close on click just to read, maybe? Or keep standard
              className={`flex gap-3 rounded-lg border border-transparent p-3 hover:bg-gray-50 dark:hover:bg-white/5 ${!notification.leida ? 'bg-blue-50/50 dark:bg-blue-900/10' : ''}`}
              href="#"
            >
              <div className="flex-shrink-0 mt-1">
                <span className={`flex items-center justify-center w-8 h-8 rounded-full ${!notification.leida ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-500'}`}>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
                </span>
              </div>

              <div className="flex-grow">
                <div className="flex justify-between items-start gap-2">
                  <span className="font-medium text-sm text-gray-800 dark:text-white/90">
                    Cambio de Estado: <span className="text-blue-600">{notification.ocid || notification.id_convocatoria}</span>
                  </span>
                  {!notification.leida && (
                    <button
                      onClick={(e) => handleMarkAsRead(e, notification.id)}
                      className="text-xs text-blue-500 hover:text-blue-700 whitespace-nowrap"
                    >
                      Marcar
                    </button>
                  )}
                </div>

                <p className="text-xs text-gray-500 mt-1">
                  {notification.estado_anterior} <span className="mx-1">→</span>
                  <span className={`font-medium ${notification.estado_nuevo === 'ADJUDICADO' ? 'text-green-600' :
                      notification.estado_nuevo === 'NULO' ? 'text-red-600' :
                        notification.estado_nuevo === 'DESIERTO' ? 'text-orange-600' : 'text-gray-700'
                    }`}>
                    {notification.estado_nuevo}
                  </span>
                </p>

                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-gray-400">
                    {new Date(notification.fecha_creacion).toLocaleDateString()}
                  </span>
                  <Link
                    href={`/busqueda-licitaciones?id=${notification.id_convocatoria}`}
                    onClick={closeDropdown}
                    className="text-xs font-semibold text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    Ver
                  </Link>
                </div>
              </div>
            </DropdownItem>
          </li>
        ))}
      </ul>

      <Link
        href="/notificaciones"
        onClick={closeDropdown}
        className="block px-4 py-2 mt-auto text-sm font-medium text-center text-gray-700 bg-gray-50 border-t border-gray-200 hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 rounded-b-2xl"
      >
        Ver todas las notificaciones
      </Link>
    </Dropdown>
  </div>
);
}
```
