'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { LogoutModal } from '@/components/ui/logout-modal';
import NotificationDropdown from '@/components/notifications/notification-dropdown';

export function HeaderActions() {
    const router = useRouter();
    const [user, setUser] = useState<any>(null);
    const [darkMode, setDarkMode] = useState(false);
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);

    useEffect(() => {
        const loadUser = () => {
            const userData = localStorage.getItem('user');
            if (userData) {
                const parsedUser = JSON.parse(userData);
                console.log('Header User Data:', parsedUser);
                setUser(parsedUser);
            }
        };

        loadUser();
        window.addEventListener('userUpdated', loadUser);

        // Dark Mode Initialization
        const isDark = localStorage.getItem('theme') === 'dark' ||
            (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);

        setDarkMode(isDark);
        if (isDark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }

        return () => window.removeEventListener('userUpdated', loadUser);
    }, []);

    const toggleTheme = () => {
        const newMode = !darkMode;
        setDarkMode(newMode);
        if (newMode) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    };

    const handleLogout = () => {
        setIsLogoutModalOpen(true);
    };

    const confirmLogout = () => {
        localStorage.clear();
        window.location.href = '/';
    };

    return (
        <>
            <div className="absolute top-6 right-6 z-50 flex items-center gap-4">
                {/* Dark Mode Toggle */}
                <button
                    onClick={toggleTheme}
                    className="w-12 h-12 rounded-full bg-white/50 dark:bg-slate-800/50 backdrop-blur-md border border-gray-200 dark:border-slate-700 shadow-lg flex items-center justify-center text-slate-700 dark:text-blue-300 hover:bg-white dark:hover:bg-slate-800 transition-all hover:scale-110 active:scale-95 group"
                    title={darkMode ? "Cambiar a Modo Claro" : "Cambiar a Modo Oscuro"}
                >
                    <i className={`fas ${darkMode ? 'fa-sun' : 'fa-moon'} text-xl transition-transform group-hover:rotate-12`}></i>
                </button>

                {/* Notifications */}
                <div className="w-12 h-12 rounded-full bg-white/50 dark:bg-slate-800/50 backdrop-blur-md border border-gray-200 dark:border-slate-700 shadow-lg flex items-center justify-center transition-all hover:scale-110 active:scale-95">
                    <NotificationDropdown />
                </div>

                {/* User Profile */}
                <div className="relative">
                    <button
                        onClick={() => setIsProfileOpen(!isProfileOpen)}
                        className="w-12 h-12 rounded-full bg-white/50 dark:bg-slate-800/50 backdrop-blur-md border border-gray-200 dark:border-slate-700 shadow-lg flex items-center justify-center text-gray-700 dark:text-gray-200 hover:bg-white dark:hover:bg-slate-800 transition-all hover:scale-110 active:scale-95 group p-0.5"
                    >
                        <div className="w-full h-full rounded-full bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center text-white text-lg font-bold shadow-md overflow-hidden">
                            {user?.avatar_url ? (
                                <img src={user.avatar_url} alt="Avatar" className="w-full h-full object-cover" />
                            ) : (
                                user?.nombre?.charAt(0).toUpperCase() || user?.username?.charAt(0).toUpperCase() || 'U'
                            )}
                        </div>
                    </button>

                    {/* Dropdown Menu */}
                    {isProfileOpen && (
                        <div className="absolute right-0 top-full mt-2 w-72 bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-gray-100 dark:border-slate-700 overflow-hidden animate-in fade-in zoom-in-95 duration-200 origin-top-right">
                            <div className="p-4 border-b border-gray-100 dark:border-slate-700 bg-gray-50/50 dark:bg-slate-900/50">
                                <p className="font-bold text-gray-900 dark:text-white mb-1">{user?.nombre || 'Usuario'}</p>
                                <p className="text-xs font-medium text-gray-600 dark:text-gray-300 mb-1">{user?.job_title || 'Sin cargo definido'}</p>
                                <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{user?.email || 'usuario@example.com'}</p>
                            </div>
                            <div className="p-2">
                                <button
                                    onClick={() => {
                                        setIsProfileOpen(false);
                                        router.push('/profile');
                                    }}
                                    className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-700/50 text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-3 transition-colors"
                                >
                                    <i className="fas fa-user-circle text-gray-400 w-5"></i> Editar perfil
                                </button>
                                <button
                                    onClick={() => {
                                        setIsProfileOpen(false);
                                        router.push('/settings');
                                    }}
                                    className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-700/50 text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-3 transition-colors"
                                >
                                    <i className="fas fa-cog text-gray-400 w-5"></i> Configuración
                                </button>
                                <button
                                    onClick={() => {
                                        setIsProfileOpen(false);
                                        router.push('/support');
                                    }}
                                    className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-700/50 text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-3 transition-colors"
                                >
                                    <i className="fas fa-circle-info text-gray-400 w-5"></i> Soporte
                                </button>
                                <div className="h-px bg-gray-100 dark:bg-slate-700 my-1"></div>
                                <button
                                    onClick={handleLogout}
                                    className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-red-50 dark:hover:bg-red-900/20 text-sm font-medium text-red-600 dark:text-red-400 flex items-center gap-3 transition-colors"
                                >
                                    <i className="fas fa-right-from-bracket w-5"></i> Cerrar Sesión
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <LogoutModal
                open={isLogoutModalOpen}
                onOpenChange={setIsLogoutModalOpen}
                onConfirm={confirmLogout}
            />
        </>
    );
}
