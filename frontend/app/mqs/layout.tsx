'use client';

import { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { HeaderActions } from '@/components/layout/header-actions';
import ChatbotWidget from '@/components/chatbot/ChatbotWidget';

export default function MQSLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    const pathname = usePathname();
    const [collapsed, setCollapsed] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [user, setUser] = useState<any>(null);
    const [darkMode, setDarkMode] = useState(false);

    useEffect(() => {
        const userData = localStorage.getItem('user');

        if (userData) {
            setUser(JSON.parse(userData));
        }

        // Dark Mode Initialization
        const isDark = localStorage.getItem('theme') === 'dark' ||
            (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);

        setDarkMode(isDark);
        if (isDark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [router]);

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

    useEffect(() => {
        setMobileMenuOpen(false);
    }, [pathname]);



    const isActive = (path: string) => pathname === path;
    const isAdmin = user?.role === 'admin';
    const getDelay = (index: number) => `${index * 50}ms`;

    return (
        <div className={`flex w-full h-screen overflow-hidden bg-[#F8FAFC] dark:bg-[#0f172a] transition-colors duration-500`}>
            {/* Overlay Móvil Glassmorphism */}
            <div
                className={`
                    fixed inset-0 z-40 md:hidden transition-all duration-500 ease-in-out
                    ${mobileMenuOpen ? 'bg-[#0F2C4A]/40 backdrop-blur-md opacity-100' : 'opacity-0 pointer-events-none'}
                `}
                onClick={() => setMobileMenuOpen(false)}
            ></div>

            {/* Sidebar Premium */}
            <aside
                className={`
                    fixed md:static inset-y-0 left-0 z-50
                    text-white flex flex-col flex-shrink-0 
                    transition-all duration-500 cubic-bezier(0.4, 0, 0.2, 1) shadow-2xl md:shadow-xl
                    /* Fondo Restaurado */
                    bg-gradient-to-b from-[#0F2C4A] via-[#133657] to-[#081829]
                    ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
                    ${collapsed ? 'w-[90px]' : 'w-[280px]'}
                    /* Bordes redondeados en escritorio */
                    md:my-4 md:ml-4 md:rounded-3xl border-r-0 md:border border-white/5
                    relative
                `}
            >
                <div className="h-[90px] flex items-center justify-between px-6 relative">
                    <div className={`transition-all duration-500 flex items-center justify-center gap-3 ${collapsed ? 'opacity-0 w-0' : 'opacity-100 flex-1'}`}>
                        {/* Logo MQS */}
                        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg backdrop-blur-sm ring-1 ring-white/20 overflow-hidden flex-shrink-0">
                            <img src="/logo-mqs.png" alt="MQS" className="w-full h-full object-cover" />
                        </div>

                        {/* Texto Marca */}
                        <span className="font-bold text-2xl tracking-tight text-white font-sans drop-shadow-md whitespace-nowrap">
                            MQS <span className="text-blue-200">JCQ</span>
                        </span>

                        {/* Logo JCQ */}
                        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg backdrop-blur-sm ring-1 ring-white/20 overflow-hidden flex-shrink-0">
                            <img src="/logo-jcq.png" alt="JCQ" className="w-full h-full object-cover" />
                        </div>
                    </div>

                    <button
                        onClick={() => setMobileMenuOpen(false)}
                        className="md:hidden w-8 h-8 flex items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
                    >
                        <i className="fas fa-times"></i>
                    </button>
                </div>

                {/* Botón Toggle Flotante en el Borde (Mitad de Altura) */}
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className={`
                        hidden md:flex items-center justify-center
                        w-6 h-12 rounded-full
                        bg-[#0F2C4A] border border-white/20 shadow-[0_0_15px_rgba(0,0,0,0.3)]
                        text-blue-200 hover:text-white hover:bg-blue-600
                        transition-all duration-300 transform hover:scale-110 active:scale-95
                        absolute -right-3 top-1/2 -translate-y-1/2 z-[60]
                        cursor-pointer backdrop-blur-md
                    `}
                    title={collapsed ? "Expandir menú" : "Colapsar menú"}
                >
                    <i className={`fas ${collapsed ? 'fa-chevron-right' : 'fa-chevron-left'} text-[10px]`}></i>
                </button>

                {/* Perfil de Usuario */}


                {/* Menú Scrollable */}
                <div className="flex-1 overflow-y-auto px-3 space-y-1 pb-4 scrollbar-hide mask-image-b">

                    <MenuGroup title="Principal" collapsed={collapsed}>
                        <MenuItem href="/mqs/obras" icon="fa-folder-open" label="Obras Secrex" active={isActive('/mqs/obras')} collapsed={collapsed} delay={getDelay(1)} />
                        <MenuItem href="/mqs/formatos" icon="fa-file-pdf" label="Formatos" active={isActive('/mqs/formatos')} collapsed={collapsed} delay={getDelay(2)} />
                    </MenuGroup>

                    <MenuGroup title="Operaciones" collapsed={collapsed} className="mt-6">
                        <MenuItem href="/mqs/renovaciones" icon="fa-clock" label="Renovaciones" active={isActive('/mqs/renovaciones')} collapsed={collapsed} delay={getDelay(3)} />
                        <MenuItem href="/mqs/fianzas" icon="fa-money-check-dollar" label="Fianzas Perú" active={isActive('/mqs/fianzas')} collapsed={collapsed} delay={getDelay(4)} />
                        <MenuItem href="/mqs/entregas" icon="fa-truck-fast" label="Entregas" active={isActive('/mqs/entregas')} collapsed={collapsed} delay={getDelay(5)} />
                        <MenuItem href="/mqs/correos" icon="fa-envelope" label="Correos" active={isActive('/mqs/correos')} collapsed={collapsed} delay={getDelay(6)} />
                    </MenuGroup>

                    {isAdmin && (
                        <MenuGroup title="Finanzas" collapsed={collapsed} className="mt-6">
                            <MenuItem href="/mqs/admin/cheques" icon="fa-money-bill-wave" label="Cheques" active={isActive('/mqs/admin/cheques')} collapsed={collapsed} delay={getDelay(7)} />
                            <MenuItem href="/mqs/admin/primas" icon="fa-hand-holding-dollar" label="Primas" active={isActive('/mqs/admin/primas')} collapsed={collapsed} delay={getDelay(8)} />
                            <MenuItem href="/mqs/admin/facturas" icon="fa-file-invoice-dollar" label="Facturas" active={isActive('/mqs/admin/facturas')} collapsed={collapsed} delay={getDelay(9)} />
                            <MenuItem href="/mqs/admin/flujo-caja" icon="fa-chart-line" label="Flujo de Caja" active={isActive('/mqs/admin/flujo-caja')} collapsed={collapsed} delay={getDelay(10)} />
                            <MenuItem href="/mqs/admin/informes" icon="fa-chart-pie" label="Informes" active={isActive('/mqs/admin/informes')} collapsed={collapsed} delay={getDelay(11)} />
                            <MenuItem href="/mqs/admin/correo-admin" icon="fa-envelope-open-text" label="Correo Admin" active={isActive('/mqs/admin/correo-admin')} collapsed={collapsed} delay={getDelay(12)} />
                        </MenuGroup>
                    )}
                </div>

                {/* Footer */}
                <div className="p-4 mt-auto space-y-3">
                    {/* Dark Mode Toggle (Footer) */}
                    <button
                        onClick={() => router.push('/modules')}
                        className={`
                            relative overflow-hidden group w-full rounded-2xl transition-all duration-300 border border-white/10 mb-3
                            ${collapsed
                                ? 'h-12 bg-white/5 hover:bg-white/20 flex items-center justify-center'
                                : 'px-4 py-3.5 bg-white/5 hover:bg-white/20 flex items-center gap-3 text-blue-100 hover:text-white'}
                        `}
                    >
                        <div className={`absolute inset-0 bg-blue-600 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ${collapsed ? 'rounded-2xl' : ''}`}></div>
                        <i className="fas fa-arrow-left relative z-10 text-lg transition-transform group-hover:-translate-x-1"></i>
                        {!collapsed && <span className="font-bold text-base relative z-10 tracking-wide">Volver</span>}
                    </button>


                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col h-screen overflow-hidden relative">
                {/* Header Actions - Top Right */}
                <HeaderActions />

                {/* Header Móvil */}

                {/* Header Móvil */}
                <div className="md:hidden m-3 h-[70px] bg-white/90 backdrop-blur-lg rounded-2xl border border-gray-100 flex items-center px-4 justify-between flex-shrink-0 sticky top-3 z-30 shadow-lg shadow-blue-900/5">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => setMobileMenuOpen(true)}
                            className="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-50 text-[#0F2C4A] hover:bg-blue-600 hover:text-white transition-all shadow-sm active:scale-90"
                        >
                            <i className="fas fa-bars text-lg"></i>
                        </button>
                        <span className="font-bold text-[#0F2C4A] text-lg tracking-tight">MQS</span>
                    </div>
                    <div className="w-9 h-9 bg-gradient-to-br from-[#0F2C4A] to-[#1a4b7a] rounded-xl text-white flex items-center justify-center text-sm font-bold shadow-md">
                        {user?.username?.charAt(0).toUpperCase() || 'U'}
                    </div>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 scroll-smooth">
                    <div className="h-full animate-in fade-in duration-700 slide-in-from-bottom-2">
                        {children}
                    </div>
                </div>
            </main>
            <ChatbotWidget />
        </div>
    );
}

function MenuGroup({ title, children, collapsed, className = "" }: any) {
    if (collapsed) return <div className={`space-y-1 mb-2 ${className}`}>{children}</div>;
    return (
        <div className={`space-y-1 mb-2 ${className}`}>
            <div className="px-4 py-2 flex items-center gap-2 opacity-80">
                <div className="h-[2px] w-3 bg-blue-400 rounded-full shadow-[0_0_5px_rgba(96,165,250,0.8)]"></div>
                <h4 className="text-[11px] font-extrabold text-blue-100 uppercase tracking-widest drop-shadow-sm">{title}</h4>
            </div>
            {children}
        </div>
    );
}

function MenuItem({ href, icon, label, active, collapsed, delay }: any) {
    return (
        <Link href={href}>
            <div
                style={{ animationDelay: delay }}
                className={`
                    relative mx-2 px-4 py-3.5 rounded-2xl cursor-pointer transition-all duration-300 group flex items-center
                    ${active
                        ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-900/40 translate-x-1 scale-[1.02]'
                        : 'text-white/80 hover:bg-white/10 hover:text-white hover:translate-x-1 hover:shadow-md hover:shadow-black/20'
                    }
                    ${collapsed ? 'justify-center px-0 py-3.5 mx-1 !rounded-xl' : ''}
                    animate-in slide-in-from-left-2 fade-in fill-mode-backwards
                `}
            >
                <i className={`fas ${icon} text-xl transition-transform duration-300 group-hover:scale-110 group-active:scale-95 ${collapsed ? '' : 'mr-4 w-6 text-center'} ${active ? 'text-white drop-shadow-md' : 'text-blue-100/70 group-hover:text-white group-hover:drop-shadow-sm'}`}></i>

                {!collapsed && (
                    <span className={`font-semibold tracking-wide flex-1 drop-shadow-sm ${active ? 'text-[15.5px]' : 'text-[15px]'}`}>{label}</span>
                )}

                {active && !collapsed && (
                    <div className="w-2 h-2 rounded-full bg-white shadow-[0_0_10px_rgba(255,255,255,1)] animate-pulse ml-2"></div>
                )}
            </div>
        </Link>
    );
}
