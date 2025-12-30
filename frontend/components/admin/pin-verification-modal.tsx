'use client';

import { useState } from 'react';
import { X } from 'lucide-react';

interface PinVerificationModalProps {
    isOpen: boolean;
    onClose: () => void;
    onVerify: (pin: string) => Promise<boolean>;
    title?: string;
    description?: string;
}

export function PinVerificationModal({
    isOpen,
    onClose,
    onVerify,
    title = "Verificación de PIN",
    description = "Para continuar, ingresa tu PIN de seguridad de 6 dígitos"
}: PinVerificationModalProps) {
    const [pin, setPin] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (pin.length !== 6 || !/^\d+$/.test(pin)) {
            setError('El PIN debe ser de 6 dígitos numéricos');
            return;
        }

        setLoading(true);
        try {
            const isValid = await onVerify(pin);
            if (!isValid) {
                setError('PIN incorrecto. Inténtalo de nuevo.');
                setPin('');
            }
        } catch (err: any) {
            setError(err.message || 'Error al verificar el PIN');
            setPin('');
        } finally {
            setLoading(false);
        }
    };

    const handleClose = () => {
        setPin('');
        setError('');
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-md p-6 relative animate-in fade-in zoom-in-95 duration-200">
                {/* Close Button */}
                <button
                    onClick={handleClose}
                    className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
                    disabled={loading}
                >
                    <X size={24} />
                </button>

                {/* Header */}
                <div className="mb-6">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                        {title}
                    </h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                        {description}
                    </p>
                </div>

                {/* PIN Form */}
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            PIN de Seguridad
                        </label>
                        <input
                            type="password"
                            value={pin}
                            onChange={(e) => {
                                const value = e.target.value.replace(/\D/g, '').slice(0, 6);
                                setPin(value);
                                setError('');
                            }}
                            placeholder="••••••"
                            maxLength={6}
                            className="w-full px-4 py-3 text-center text-2xl tracking-widest border border-gray-300 dark:border-slate-600 rounded-xl bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                            disabled={loading}
                            autoFocus
                        />
                        {pin.length > 0 && (
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                                {pin.length}/6 dígitos
                            </p>
                        )}
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
                            <p className="text-sm text-red-600 dark:text-red-400 text-center">
                                {error}
                            </p>
                        </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex gap-3">
                        <button
                            type="button"
                            onClick={handleClose}
                            className="flex-1 px-4 py-3 border border-gray-300 dark:border-slate-600 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors font-medium"
                            disabled={loading}
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={pin.length !== 6 || loading}
                            className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                        >
                            {loading ? 'Verificando...' : 'Verificar PIN'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
