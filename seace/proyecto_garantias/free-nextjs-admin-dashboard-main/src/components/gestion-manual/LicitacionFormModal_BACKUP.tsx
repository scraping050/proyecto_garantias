"use client";
import React, { useState, useEffect } from "react";
import type { Licitacion } from "@/types/licitacion";

interface LicitacionFormModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: (data: Partial<Licitacion>) => Promise<void>;
    licitacion?: Licitacion | null;
    mode: "create" | "edit";
}

export const LicitacionFormModal: React.FC<LicitacionFormModalProps> = ({
    isOpen,
    onClose,
    onSave,
    licitacion,
    mode,
}) => {
    const [isSaving, setIsSaving] = useState(false);
    const [formData, setFormData] = useState<Partial<Licitacion>>({
        descripcion: "",
        comprador: "",
        departamento: "",
        provincia: "",
        distrito: "",
        estado_proceso: "",
        categoria: "",
        monto_estimado: 0,
        monto_total_adjudicado: 0,
        fecha_publicacion: "",
        fecha_adjudicacion: "",
        nomenclatura: "",
        ocid: "",
        tipo_procedimiento: "",
        ganadores: "",
        ganadores_ruc: "",
        tipos_garantia: "",
        entidades_financieras: "",
        moneda: "PEN",
        estado_item: "",
    });

    // Load licitacion data when editing
    useEffect(() => {
        if (mode === "edit" && licitacion) {
            setFormData({
                descripcion: licitacion.descripcion || "",
                comprador: licitacion.comprador || "",
                departamento: licitacion.departamento || "",
                provincia: licitacion.provincia || "",
                distrito: licitacion.distrito || "",
                estado_proceso: licitacion.estado_proceso || "",
                categoria: licitacion.categoria || "",
                monto_estimado: licitacion.monto_estimado || 0,
                monto_total_adjudicado: licitacion.monto_total_adjudicado || 0,
                fecha_publicacion: licitacion.fecha_publicacion || "",
                fecha_adjudicacion: licitacion.fecha_adjudicacion || "",
                nomenclatura: licitacion.nomenclatura || "",
                ocid: licitacion.ocid || "",
                tipo_procedimiento: licitacion.tipo_procedimiento || "",
                ganadores: licitacion.ganadores || "",
                ganadores_ruc: licitacion.ganadores_ruc || "",
                tipos_garantia: licitacion.tipos_garantia || "",
                entidades_financieras: licitacion.entidades_financieras || "",
                moneda: licitacion.moneda || "PEN",
                estado_item: licitacion.estado_item || "",
            });
        } else if (mode === "create") {
            // Reset form for create mode
            setFormData({
                descripcion: "",
                comprador: "",
                departamento: "",
                provincia: "",
                distrito: "",
                estado_proceso: "",
                categoria: "",
                monto_estimado: 0,
                monto_total_adjudicado: 0,
                fecha_publicacion: "",
                fecha_adjudicacion: "",
                nomenclatura: "",
                ocid: "",
                tipo_procedimiento: "",
                ganadores: "",
                ganadores_ruc: "",
                tipos_garantia: "",
                entidades_financieras: "",
                moneda: "PEN",
                estado_item: "",
            });
        }
    }, [mode, licitacion, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSaving(true);
        try {
            await onSave(formData);
            onClose();
        } catch (error) {
            console.error("Error saving:", error);
            alert("Error al guardar la licitación");
        } finally {
            setIsSaving(false);
        }
    };

    const handleChange = (field: keyof Licitacion, value: any) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[9999] overflow-y-auto">
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
                onClick={onClose}
                aria-hidden="true"
            />

            {/* Modal Container - Centered */}
            <div className="flex min-h-full items-center justify-center p-4">
                {/* Modal */}
                <div className="relative my-8 w-full max-w-4xl rounded-2xl border border-gray-200 bg-white shadow-2xl dark:border-gray-700 dark:bg-gray-900 transform transition-all">
                    {/* Header */}
                    <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4 dark:border-gray-700">
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                            {mode === "create" ? "Nueva Licitación" : "Editar Licitación"}
                        </h2>
                        <button
                            onClick={onClose}
                            type="button"
                            className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-800 dark:hover:text-gray-300"
                        >
                            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </button>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="p-4 sm:p-6">
                        {/* Scroll container with visual indicators */}
                        <div className="relative">
                            {/* Top shadow indicator */}
                            <div className="pointer-events-none absolute left-0 right-0 top-0 z-10 h-4 bg-gradient-to-b from-white to-transparent dark:from-gray-900" />

                            <div className="max-h-[60vh] space-y-5 overflow-y-auto px-1 py-2 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100 dark:scrollbar-thumb-gray-600 dark:scrollbar-track-gray-800">
                                {/* Información Básica */}
                                <div className="space-y-4">
                                    <div className="border-b border-gray-200 pb-2 dark:border-gray-700">
                                        <h3 className="text-sm font-medium uppercase tracking-wide text-gray-700 dark:text-gray-300">
                                            Información Básica
                                        </h3>
                                    </div>
                                    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Descripción *
                                            </label>
                                            <textarea
                                                value={formData.descripcion}
                                                onChange={(e) => handleChange("descripcion", e.target.value)}
                                                required
                                                rows={3}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Comprador *
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.comprador}
                                                onChange={(e) => handleChange("comprador", e.target.value)}
                                                required
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Nomenclatura
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.nomenclatura}
                                                onChange={(e) => handleChange("nomenclatura", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                OCID
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.ocid}
                                                onChange={(e) => handleChange("ocid", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Ubicación */}
                                <div className="space-y-4">
                                    <div className="border-b border-gray-200 pb-2 dark:border-gray-700">
                                        <h3 className="text-sm font-medium uppercase tracking-wide text-gray-700 dark:text-gray-300">
                                            Ubicación
                                        </h3>
                                    </div>
                                    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Departamento *
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.departamento}
                                                onChange={(e) => handleChange("departamento", e.target.value)}
                                                required
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Provincia
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.provincia}
                                                onChange={(e) => handleChange("provincia", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Distrito
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.distrito}
                                                onChange={(e) => handleChange("distrito", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Categorización */}
                                <div className="space-y-4">
                                    <div className="border-b border-gray-200 pb-2 dark:border-gray-700">
                                        <h3 className="text-sm font-medium uppercase tracking-wide text-gray-700 dark:text-gray-300">
                                            Categorización
                                        </h3>
                                    </div>
                                    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Estado del Proceso *
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.estado_proceso}
                                                onChange={(e) => handleChange("estado_proceso", e.target.value)}
                                                required
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Categoría *
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.categoria}
                                                onChange={(e) => handleChange("categoria", e.target.value)}
                                                required
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Tipo de Procedimiento
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.tipo_procedimiento}
                                                onChange={(e) => handleChange("tipo_procedimiento", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Montos y Fechas */}
                                <div className="space-y-4">
                                    <div className="border-b border-gray-200 pb-2 dark:border-gray-700">
                                        <h3 className="text-sm font-medium uppercase tracking-wide text-gray-700 dark:text-gray-300">
                                            Montos y Fechas
                                        </h3>
                                    </div>
                                    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Monto Estimado (S/)
                                            </label>
                                            <input
                                                type="number"
                                                step="0.01"
                                                value={formData.monto_estimado}
                                                onChange={(e) => handleChange("monto_estimado", parseFloat(e.target.value) || 0)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Monto Adjudicado (S/)
                                            </label>
                                            <input
                                                type="number"
                                                step="0.01"
                                                value={formData.monto_total_adjudicado}
                                                onChange={(e) => handleChange("monto_total_adjudicado", parseFloat(e.target.value) || 0)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Fecha de Publicación
                                            </label>
                                            <input
                                                type="date"
                                                value={formData.fecha_publicacion ? formData.fecha_publicacion.split('T')[0] : ''}
                                                onChange={(e) => handleChange("fecha_publicacion", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Fecha de Adjudicación
                                            </label>
                                            <input
                                                type="date"
                                                value={formData.fecha_adjudicacion ? formData.fecha_adjudicacion.split('T')[0] : ''}
                                                onChange={(e) => handleChange("fecha_adjudicacion", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Ganadores y Garantías */}
                                <div className="space-y-4">
                                    <div className="border-b border-gray-200 pb-2 dark:border-gray-700">
                                        <h3 className="text-sm font-medium uppercase tracking-wide text-gray-700 dark:text-gray-300">
                                            Ganadores y Garantías
                                        </h3>
                                    </div>
                                    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Ganador
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.ganadores}
                                                onChange={(e) => handleChange("ganadores", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                RUC Ganador
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.ganadores_ruc}
                                                onChange={(e) => handleChange("ganadores_ruc", e.target.value)}
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Tipos de Garantía
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.tipos_garantia}
                                                onChange={(e) => handleChange("tipos_garantia", e.target.value)}
                                                placeholder="Ej: GARANTIA_BANCARIA, RETENCION"
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                                Entidades Financieras
                                            </label>
                                            <input
                                                type="text"
                                                value={formData.entidades_financieras}
                                                onChange={(e) => handleChange("entidades_financieras", e.target.value)}
                                                placeholder="Ej: BCP, BBVA"
                                                className="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Bottom shadow indicator */}
                            <div className="pointer-events-none absolute bottom-0 left-0 right-0 z-10 h-4 bg-gradient-to-t from-white to-transparent dark:from-gray-900" />
                        </div>

                        {/* Footer Actions */}
                        <div className="mt-4 flex flex-col gap-3 border-t border-gray-200 pt-4 dark:border-gray-700 sm:mt-6 sm:flex-row sm:pt-6">
                            <button
                                type="button"
                                onClick={onClose}
                                disabled={isSaving}
                                className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
                            >
                                Cancelar
                            </button>
                            <button
                                type="submit"
                                disabled={isSaving}
                                className="flex-1 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                {isSaving ? (
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
                                        Guardando...
                                    </span>
                                ) : (
                                    mode === "create" ? "Crear Licitación" : "Guardar Cambios"
                                )}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

