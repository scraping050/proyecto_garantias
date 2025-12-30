import { X, AlertTriangle } from 'lucide-react';

interface ConfirmationModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void;
    title: string;
    description: string;
    confirmText?: string;
    cancelText?: string;
    variant?: 'danger' | 'warning' | 'info';
}

export function ConfirmationModal({
    isOpen,
    onClose,
    onConfirm,
    title,
    description,
    confirmText = 'Aceptar',
    cancelText = 'Cancelar',
    variant = 'danger'
}: ConfirmationModalProps) {
    if (!isOpen) return null;

    const colors = {
        danger: {
            iconBg: 'bg-red-100 dark:bg-red-900/30',
            iconColor: 'text-red-600 dark:text-red-400',
            buttonBg: 'bg-red-600 hover:bg-red-700 shadow-red-500/30',
        },
        warning: {
            iconBg: 'bg-amber-100 dark:bg-amber-900/30',
            iconColor: 'text-amber-600 dark:text-amber-400',
            buttonBg: 'bg-amber-600 hover:bg-amber-700 shadow-amber-500/30',
        },
        info: {
            iconBg: 'bg-blue-100 dark:bg-blue-900/30',
            iconColor: 'text-blue-600 dark:text-blue-400',
            buttonBg: 'bg-blue-600 hover:bg-blue-700 shadow-blue-500/30',
        }
    };

    const currentStyle = colors[variant];

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
            <div className="bg-white dark:bg-slate-800 rounded-2xl w-full max-w-md shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden animate-in zoom-in-95 duration-200">
                {/* Header */}
                <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
                    <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-full ${currentStyle.iconBg} flex items-center justify-center ${currentStyle.iconColor}`}>
                            <AlertTriangle size={20} />
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 dark:text-white">{title}</h3>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-full text-slate-500 transition-colors"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Body */}
                <div className="p-6 text-center">
                    <p className="text-slate-600 dark:text-slate-300 text-lg mb-2">
                        {description}
                    </p>
                    <p className="text-sm text-slate-400">
                        Esta acción no se puede deshacer.
                    </p>
                </div>

                {/* Footer */}
                <div className="p-6 pt-0 flex flex-col gap-3">
                    <button
                        onClick={onConfirm}
                        className={`w-full py-3.5 rounded-xl font-bold text-white shadow-lg transition-all hover:scale-[1.02] active:scale-[0.98] ${currentStyle.buttonBg}`}
                    >
                        {confirmText}
                    </button>
                    <button
                        onClick={onClose}
                        className="w-full py-3.5 rounded-xl font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors"
                    >
                        {cancelText}
                    </button>
                </div>
            </div>
        </div>
    );
}
