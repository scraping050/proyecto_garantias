"use client";

import React from 'react';
import ChatbotWidget from '@/components/chatbot/ChatbotWidget';
import { Bot, Database, Mic, Terminal } from 'lucide-react';

export default function AuraPage() {
    return (
        <div className="relative min-h-[80vh] flex flex-col items-center justify-center p-6 bg-gray-50 dark:bg-zinc-900 rounded-3xl overflow-hidden border border-gray-200 dark:border-zinc-800">

            {/* Background Decor */}
            <div className="absolute inset-0 z-0">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse [animation-delay:1s]"></div>
            </div>

            <div className="z-10 text-center space-y-8 max-w-2xl">

                {/* Header */}
                <div className="flex flex-col items-center gap-4">
                    <div className="p-4 bg-white dark:bg-zinc-800 rounded-2xl shadow-xl shadow-blue-500/20 border border-gray-100 dark:border-zinc-700">
                        <Bot className="w-16 h-16 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h1 className="text-5xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-violet-600 dark:from-blue-400 dark:to-violet-400">
                        Módulo AURA
                    </h1>
                    <p className="text-xl text-gray-500 dark:text-gray-400 font-medium">
                        Tu copiloto inteligente para Garantías SEACE
                    </p>
                </div>

                {/* Status Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
                    <div className="p-4 bg-white dark:bg-zinc-800 rounded-xl border border-gray-200 dark:border-zinc-700 shadow-sm flex items-center gap-3">
                        <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg text-green-600 dark:text-green-400">
                            <Database className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-bold text-gray-700 dark:text-gray-200 text-sm">Base de Datos</h3>
                            <p className="text-xs text-green-600 dark:text-green-400 font-medium">Conectado</p>
                        </div>
                    </div>

                    <div className="p-4 bg-white dark:bg-zinc-800 rounded-xl border border-gray-200 dark:border-zinc-700 shadow-sm flex items-center gap-3">
                        <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg text-blue-600 dark:text-blue-400">
                            <Terminal className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-bold text-gray-700 dark:text-gray-200 text-sm">Modelo IA</h3>
                            <p className="text-xs text-blue-600 dark:text-blue-400 font-medium">Llama 3 (Groq)</p>
                        </div>
                    </div>

                    <div className="p-4 bg-white dark:bg-zinc-800 rounded-xl border border-gray-200 dark:border-zinc-700 shadow-sm flex items-center gap-3">
                        <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg text-purple-600 dark:text-purple-400">
                            <Mic className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-bold text-gray-700 dark:text-gray-200 text-sm">Voz</h3>
                            <p className="text-xs text-purple-600 dark:text-purple-400 font-medium">Web Speech API</p>
                        </div>
                    </div>
                </div>

                {/* Instructions */}
                <div className="p-6 bg-white/50 dark:bg-zinc-800/50 backdrop-blur-sm rounded-2xl border border-dashed border-gray-300 dark:border-zinc-700">
                    <h3 className="font-bold text-gray-700 dark:text-gray-200 mb-2">¿Cómo empezar?</h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                        AURA ya está activa en la esquina inferior derecha de tu pantalla.
                        Puedes navegar por cualquier parte del sistema y AURA te acompañará.
                        Haz clic en el avatar flotante para abrir el chat.
                    </p>
                </div>

            </div>
        </div>
    );
}
