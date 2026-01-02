"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import {
    Search,
    Home,
    FileText,
    Search as SearchIcon,
    BarChart,
    Bell,
    Settings,
    Moon,
    Sun,
    LogOut,
    Command,
    X
} from "lucide-react";
import { useTheme } from "@/context/ThemeContext";

interface CommandPaletteProps {
    isOpen: boolean;
    onClose: () => void;
}

interface CommandItem {
    id: string;
    label: string;
    icon: React.ReactNode;
    shortcut?: string;
    section: "Navegación" | "Acciones" | "Sistema";
    action: () => void;
}

export default function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
    const router = useRouter();
    const { theme, toggleTheme } = useTheme();
    const [query, setQuery] = useState("");
    const [selectedIndex, setSelectedIndex] = useState(0);
    const inputRef = useRef<HTMLInputElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    // Initial Commands Configuration
    const commands: CommandItem[] = [
        // Navigation
        {
            id: "nav-home",
            label: "Ir al Inicio",
            icon: <Home className="w-4 h-4" />,
            section: "Navegación",
            action: () => router.push("/")
        },
        {
            id: "nav-manual",
            label: "Gestión Manual",
            icon: <FileText className="w-4 h-4" />,
            section: "Navegación",
            action: () => router.push("/gestion-manual")
        },
        {
            id: "nav-search",
            label: "Búsqueda de Licitaciones",
            icon: <SearchIcon className="w-4 h-4" />,
            section: "Navegación",
            action: () => router.push("/busqueda-licitaciones")
        },
        {
            id: "nav-reports",
            label: "Reportes",
            icon: <BarChart className="w-4 h-4" />,
            section: "Navegación",
            action: () => router.push("/reportes")
        },
        {
            id: "nav-notifications",
            label: "Notificaciones",
            icon: <Bell className="w-4 h-4" />,
            section: "Navegación",
            action: () => router.push("/notificaciones")
        },

        // Actions
        {
            id: "act-theme",
            label: theme === 'dark' ? "Cambiar a Modo Claro" : "Cambiar a Modo Oscuro",
            icon: theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />,
            section: "Acciones",
            action: toggleTheme
        },

        // System
        {
            id: "sys-logout",
            label: "Cerrar Sesión",
            icon: <LogOut className="w-4 h-4" />,
            section: "Sistema",
            action: () => {
                // Here we can call the logout logic
                console.log("Logout triggered");
                router.push("/signin");
            }
        }
    ];

    // Filter commands based on query
    const filteredCommands = commands.filter(cmd =>
        cmd.label.toLowerCase().includes(query.toLowerCase())
    );

    // Group by section
    const groupedCommands = filteredCommands.reduce((acc, cmd) => {
        if (!acc[cmd.section]) acc[cmd.section] = [];
        acc[cmd.section].push(cmd);
        return acc;
    }, {} as Record<string, CommandItem[]>);

    // Initial focus and reset
    useEffect(() => {
        if (isOpen) {
            setQuery("");
            setSelectedIndex(0);
            setTimeout(() => inputRef.current?.focus(), 50);
        }
    }, [isOpen]);

    // Keyboard navigation
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (!isOpen) return;

            if (e.key === "ArrowDown") {
                e.preventDefault();
                setSelectedIndex(prev => (prev + 1) % filteredCommands.length);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % filteredCommands.length);
            } else if (e.key === "Enter") {
                e.preventDefault();
                if (filteredCommands[selectedIndex]) {
                    handleSelect(filteredCommands[selectedIndex]);
                }
            } else if (e.key === "Escape") {
                e.preventDefault();
                onClose();
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [isOpen, filteredCommands, selectedIndex]);

    const handleSelect = (cmd: CommandItem) => {
        cmd.action();
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div
            className="fixed inset-0 z-[99999] flex items-start justify-center pt-[15vh] px-4 backdrop-blur-sm bg-black/40 animate-in fade-in duration-200"
            onClick={(e) => {
                if (e.target === e.currentTarget) onClose();
            }}
        >
            <div
                ref={containerRef}
                className="w-full max-w-xl bg-white dark:bg-zinc-900 rounded-xl shadow-2xl border border-gray-200 dark:border-zinc-800 overflow-hidden flex flex-col animate-in slide-in-from-top-4 duration-300"
            >
                {/* Header / Input */}
                <div className="flex items-center px-4 py-3 border-b border-gray-100 dark:border-zinc-800 gap-3">
                    <Search className="w-5 h-5 text-gray-400" />
                    <input
                        ref={inputRef}
                        type="text"
                        placeholder="Escribe un comando o busca..."
                        className="flex-1 bg-transparent text-lg border-none outline-none text-gray-800 dark:text-gray-100 placeholder:text-gray-400"
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value);
                            setSelectedIndex(0);
                        }}
                    />
                    <div className="flex items-center gap-2">
                        <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-zinc-700 px-1.5 py-0.5 rounded">ESC</span>
                    </div>
                </div>

                {/* List */}
                <div className="max-h-[60vh] overflow-y-auto p-2">
                    {Object.keys(groupedCommands).map((section) => (
                        <div key={section} className="mb-2">
                            <h3 className="text-xs font-semibold text-gray-400 px-3 py-2 uppercase tracking-wider">
                                {section}
                            </h3>
                            <div className="space-y-1">
                                {groupedCommands[section].map((cmd, sectionIndex) => {
                                    // Calculate global index for highlight
                                    // This is a bit hacky but works for linear list navigation visualization
                                    const globalIndex = filteredCommands.findIndex(c => c.id === cmd.id);
                                    const isSelected = globalIndex === selectedIndex;

                                    return (
                                        <button
                                            key={cmd.id}
                                            onClick={() => handleSelect(cmd)}
                                            onMouseEnter={() => setSelectedIndex(globalIndex)}
                                            className={`w-full flex items-center gap-3 px-3 py-3 text-sm font-medium rounded-lg transition-colors ${isSelected
                                                    ? "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300"
                                                    : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-zinc-800/50"
                                                }`}
                                        >
                                            <div className={`p-2 rounded-md ${isSelected ? "bg-white dark:bg-indigo-900/50 shadow-sm" : "bg-gray-100 dark:bg-zinc-800"
                                                }`}>
                                                {cmd.icon}
                                            </div>
                                            <span className="flex-1 text-left">{cmd.label}</span>
                                            {isSelected && <span className="text-indigo-400 text-xs">↩</span>}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    ))}

                    {filteredCommands.length === 0 && (
                        <div className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                            <p>No se encontraron comandos.</p>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="bg-gray-50 dark:bg-zinc-950/50 px-4 py-2 border-t border-gray-100 dark:border-zinc-800 flex items-center justify-between text-xs text-gray-400">
                    <div className="flex gap-4">
                        <span className="flex items-center gap-1">
                            <span className="font-bold">↑↓</span> navegar
                        </span>
                        <span className="flex items-center gap-1">
                            <span className="font-bold">↵</span> seleccionar
                        </span>
                    </div>
                    <div>
                        MQS Command Palette
                    </div>
                </div>
            </div>
        </div>
    );
}
