"use client";
import React, { useState } from "react";
import type { Licitacion } from "@/types/licitacion";

interface DeleteConfirmationModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: (authCode: string) => void;
    licitacion: Licitacion | null;
    isDeleting?: boolean;
}

export const DeleteConfirmationModal: React.FC<DeleteConfirmationModalProps> = ({
    isOpen,
    onClose,
    onConfirm,
    licitacion,
    isDeleting = false,
}) => {
    const [authCode, setAuthCode] = useState("");
    const [error, setError] = useState("");

    const handleConfirm = () => {
        if (!authCode.trim()) {
            setError("Debe ingresar el código de autorización");
            return;
        }
        setError("");
        onConfirm(authCode);
    };

    const handleClose = () => {
        setAuthCode("");
        setError("");
        onClose();
    };

    if (!isOpen || !licitacion) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/50 backdrop-blur-sm"
                onClick={handleClose}
            />

            {/* Modal */}
            <div className="relative w-full max-w-md rounded-2xl border border-gray-200 bg-white p-4 shadow-2xl dark:border-gray-700 dark:bg-gray-900 sm:p-6">
                {/* Icon */}
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
                    <svg
                        className="h-6 w-6 text-red-600 dark:text-red-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                        />
                    </svg>
                </div>

                {/* Title */}
                <h3 className="mt-4 text-center text-lg font-semibold text-gray-900 dark:text-white">
                    ¿Eliminar Licitación?
                </h3>

                {/* Description */}
                <div className="mt-4 space-y-2">
                    <p className="text-center text-sm text-gray-600 dark:text-gray-400">
                        Esta acción no se puede deshacer. La licitación será eliminada permanentemente.
                    </p>

                    {/* Licitacion Info */}
                    <div className="mt-4 rounded-lg bg-gray-50 p-4 dark:bg-gray-800">
                        <div className="space-y-2 text-sm">
                            <div>
                                <span className="font-medium text-gray-700 dark:text-gray-300">ID:</span>{" "}
                                <span className="text-gray-600 dark:text-gray-400">{licitacion.id_convocatoria}</span>
                            </div>
                            <div>
                                <span className="font-medium text-gray-700 dark:text-gray-300">Descripción:</span>{" "}
                                <span className="text-gray-600 dark:text-gray-400 line-clamp-2">
                                    {licitacion.descripcion}
                                </span>
                            </div>
                            {licitacion.comprador && (
                                <div>
                                    <span className="font-medium text-gray-700 dark:text-gray-300">Comprador:</span>{" "}
                                    <span className="text-gray-600 dark:text-gray-400 line-clamp-1">
                                        {licitacion.comprador}
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Authorization Code Input */}
                    <div className="mt-4">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            <span className="flex items-center gap-2">
                                <svg className="h-4 w-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                                Código de Autorización *
                            </span>
                        </label>
                        <input
                            type="password"
                            value={authCode}
                            onChange={(e) => {
                                setAuthCode(e.target.value);
                                setError("");
                            }}
                            placeholder="Ingrese el código de autorización"
                            disabled={isDeleting}
                            className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-red-500 focus:ring-2 focus:ring-red-500/20 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                            autoFocus
                        />
                        {error && (
                            <p className="mt-2 text-sm text-red-600 dark:text-red-400 flex items-center gap-1">
                                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                {error}
                            </p>
                        )}
                    </div>
                </div>

                {/* Actions */}
                <div className="mt-6 flex gap-3">
                    <button
                        onClick={handleClose}
                        disabled={isDeleting}
                        className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                    >
                        Cancelar
                    </button>
                    <button
                        onClick={handleConfirm}
                        disabled={isDeleting || !authCode.trim()}
                        className="flex-1 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {isDeleting ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                    <circle
                                        className="opacity-25"
                                        cx="12"
                                        cy="12"
                                        r="10"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                    />
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    />
                                </svg>
                                Eliminando...
                            </span>
                        ) : (
                            "Eliminar"
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};
