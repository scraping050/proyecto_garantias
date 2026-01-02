"use client";
import React, { useState, useEffect } from "react";
import type { Licitacion, AdjudicacionDetalle, ConsorcioMember } from "@/types/licitacion";

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
    const [isLoadingDetails, setIsLoadingDetails] = useState(false);
    const [activeTab, setActiveTab] = useState<"general" | "adjudicaciones">("general");

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
        fecha_adjudicacion: "", // Fecha General
        nomenclatura: "",
        ocid: "",
        tipo_procedimiento: "Licitación Pública",
        moneda: "PEN",
        adjudicaciones: []
    });

    // Fetch details when editing
    useEffect(() => {
        const loadDetails = async () => {
            if (mode === "edit" && licitacion?.id_convocatoria) {
                setIsLoadingDetails(true);
                try {
                    const response = await fetch(`http://localhost:5000/api/licitaciones/${licitacion.id_convocatoria}`);
                    const result = await response.json();

                    if (result.success && result.data) {
                        const fullData = result.data;
                        const mappedAdjudicaciones: AdjudicacionDetalle[] = (fullData.adjudicaciones || []).map((adj: any) => {
                            const members = (fullData.consorcios || []).filter((c: any) => c.id_contrato === adj.id_contrato);
                            return {
                                id_adjudicacion: adj.id_adjudicacion,
                                id_contrato: adj.id_contrato,
                                ganador_nombre: adj.ganador_nombre,
                                ganador_ruc: adj.ganador_ruc,
                                monto_adjudicado: parseFloat(adj.monto_adjudicado),
                                fecha_adjudicacion: adj.fecha_adjudicacion, // Fecha Especifica Item
                                estado_item: adj.estado_item,
                                entidad_financiera: adj.entidad_financiera,
                                tipo_garantia: adj.tipo_garantia,
                                consorcios: members.map((m: any) => ({
                                    nombre_miembro: m.nombre_miembro,
                                    ruc_miembro: m.ruc_miembro,
                                    porcentaje_participacion: parseFloat(m.porcentaje_participacion)
                                }))
                            };
                        });

                        setFormData({
                            ...fullData.licitacion,
                            adjudicaciones: mappedAdjudicaciones
                        });
                    }
                } catch (error) {
                    console.error("Failed to load details:", error);
                } finally {
                    setIsLoadingDetails(false);
                }
            } else if (mode === "create") {
                setFormData({
                    descripcion: "",
                    comprador: "",
                    departamento: "",
                    provincia: "",
                    distrito: "",
                    estado_proceso: "CONVOCADO",
                    categoria: "",
                    monto_estimado: 0,
                    monto_total_adjudicado: 0,
                    fecha_publicacion: new Date().toISOString().split('T')[0],
                    moneda: "PEN",
                    tipo_procedimiento: "Licitación Pública",
                    adjudicaciones: []
                });
            }
        };

        if (isOpen) {
            loadDetails();
            setActiveTab("general");
        }
    }, [mode, licitacion, isOpen]);

    const handleSubmit = async (e: React.FormEvent | React.MouseEvent) => {
        if (e && e.type === 'submit') {
            e.preventDefault();
        }

        // Manual Validation
        const requiredFields = [
            { field: 'descripcion', label: 'Descripción' },
            { field: 'comprador', label: 'Comprador' },
            { field: 'departamento', label: 'Departamento' },
            { field: 'estado_proceso', label: 'Estado Proceso' },
            { field: 'categoria', label: 'Categoría' }
        ];

        const missing = requiredFields.filter(item => !formData[item.field as keyof Licitacion]);

        if (missing.length > 0) {
            alert(`Por favor complete los siguientes campos obligatorios:\n${missing.map(m => m.label).join(', ')}`);
            setActiveTab("general"); // Switch to general tab to show errors
            return;
        }

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

    // Adjudicaciones Management
    const addAdjudicacion = () => {
        const newAdj: AdjudicacionDetalle = {
            id_adjudicacion: undefined,
            id_contrato: "",
            ganador_nombre: "",
            ganador_ruc: "",
            monto_adjudicado: 0,
            estado_item: "ADJUDICADO",
            fecha_adjudicacion: new Date().toISOString().split('T')[0],
            tipo_garantia: "",
            entidad_financiera: "",
            consorcios: []
        };
        setFormData(prev => ({
            ...prev,
            adjudicaciones: [...(prev.adjudicaciones || []), newAdj]
        }));
    };

    const removeAdjudicacion = (index: number) => {
        setFormData(prev => ({
            ...prev,
            adjudicaciones: (prev.adjudicaciones || []).filter((_, i) => i !== index)
        }));
    };

    const updateAdjudicacion = (index: number, field: keyof AdjudicacionDetalle, value: any) => {
        const newAdjs = [...(formData.adjudicaciones || [])];
        newAdjs[index] = { ...newAdjs[index], [field]: value };
        setFormData(prev => ({ ...prev, adjudicaciones: newAdjs }));
    };

    const addConsorcioMember = (adjIndex: number) => {
        const newAdjs = [...(formData.adjudicaciones || [])];
        const currentMembers = newAdjs[adjIndex].consorcios || [];
        newAdjs[adjIndex].consorcios = [...currentMembers, { nombre_miembro: "", ruc_miembro: "", porcentaje_participacion: 0 }];
        setFormData(prev => ({ ...prev, adjudicaciones: newAdjs }));
    };

    const updateConsorcioMember = (adjIndex: number, memberIndex: number, field: keyof ConsorcioMember, value: any) => {
        const newAdjs = [...(formData.adjudicaciones || [])];
        if (newAdjs[adjIndex].consorcios) {
            newAdjs[adjIndex].consorcios![memberIndex] = { ...newAdjs[adjIndex].consorcios![memberIndex], [field]: value };
            setFormData(prev => ({ ...prev, adjudicaciones: newAdjs }));
        }
    };

    const removeConsorcioMember = (adjIndex: number, memberIndex: number) => {
        const newAdjs = [...(formData.adjudicaciones || [])];
        if (newAdjs[adjIndex].consorcios) {
            newAdjs[adjIndex].consorcios = newAdjs[adjIndex].consorcios!.filter((_, i) => i !== memberIndex);
            setFormData(prev => ({ ...prev, adjudicaciones: newAdjs }));
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[99999] overflow-y-auto">
            <div className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" onClick={onClose} />

            <div className="flex min-h-full items-center justify-center p-4">
                <div className="relative my-8 w-full max-w-5xl rounded-2xl border border-gray-200 bg-white shadow-2xl dark:border-gray-700 dark:bg-gray-900 flex flex-col max-h-[90vh]">

                    {/* Header */}
                    <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4 dark:border-gray-700 shrink-0">
                        <div>
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                                {mode === "create" ? "Nueva Licitación" : "Editar Licitación"}
                            </h2>
                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                {mode === "edit" ? "Modifique los detalles y adjudicaciones." : "Complete la información para registrar una nueva licitación."}
                            </p>
                        </div>
                        <button onClick={onClose} className="rounded-lg p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800">
                            ✕
                        </button>
                    </div>

                    {/* Tabs */}
                    <div className="flex border-b border-gray-200 px-6 dark:border-gray-700 shrink-0">
                        <button
                            onClick={() => setActiveTab("general")}
                            className={`mr-4 border-b-2 py-3 text-sm font-medium transition-colors ${activeTab === "general"
                                ? "border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400"
                                : "border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
                                }`}
                        >
                            📋 Información General
                        </button>
                        <button
                            onClick={() => setActiveTab("adjudicaciones")}
                            className={`border-b-2 py-3 text-sm font-medium transition-colors ${activeTab === "adjudicaciones"
                                ? "border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400"
                                : "border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
                                }`}
                        >
                            🏆 Adjudicaciones y Consorcios
                        </button>
                    </div>

                    {/* Content (Scrollable) */}
                    <div className="flex-1 overflow-y-auto p-6">
                        {isLoadingDetails ? (
                            <div className="flex h-40 items-center justify-center">
                                <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
                            </div>
                        ) : (
                            <form id="licitacion-form" onSubmit={handleSubmit} className="space-y-6">

                                {/* TAB 1: GENERAL */}
                                {activeTab === "general" && (
                                    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                                        <div className="md:col-span-2">
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Descripción *</label>
                                            <textarea
                                                required
                                                rows={2}
                                                placeholder="Ej: SERVICIO DE MANTENIMIENTO DE CARRETERAS..."
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.descripcion || ''}
                                                onChange={(e) => handleChange("descripcion", e.target.value)}
                                            />
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Comprador *</label>
                                            <input
                                                type="text"
                                                required
                                                placeholder="Ej: MUNICIPALIDAD DISTRITAL DE..."
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.comprador || ''}
                                                onChange={(e) => handleChange("comprador", e.target.value)}
                                            />
                                        </div>
                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Nomenclatura</label>
                                            <input
                                                type="text"
                                                placeholder="Ej: LP-SM-2024-001"
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.nomenclatura || ''}
                                                onChange={(e) => handleChange("nomenclatura", e.target.value)}
                                            />
                                        </div>
                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">OCID</label>
                                            <input
                                                type="text"
                                                placeholder="Ej: ocid-2024-..."
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.ocid || ''}
                                                onChange={(e) => handleChange("ocid", e.target.value)}
                                            />
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Departamento *</label>
                                            <input
                                                type="text"
                                                required
                                                placeholder="Ej: LIMA"
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.departamento || ''}
                                                onChange={(e) => handleChange("departamento", e.target.value)}
                                            />
                                        </div>
                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Provincia / Distrito</label>
                                            <div className="flex gap-2">
                                                <input
                                                    type="text"
                                                    placeholder="Ej: LIMA"
                                                    className="w-1/2 rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                    value={formData.provincia || ''}
                                                    onChange={(e) => handleChange("provincia", e.target.value)}
                                                />
                                                <input
                                                    type="text"
                                                    placeholder="Ej: MIRAFLORES"
                                                    className="w-1/2 rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                    value={formData.distrito || ''}
                                                    onChange={(e) => handleChange("distrito", e.target.value)}
                                                />
                                            </div>
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Tipo Procedimiento</label>
                                            <select
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.tipo_procedimiento || 'Licitación Pública'}
                                                onChange={(e) => handleChange("tipo_procedimiento", e.target.value)}
                                            >
                                                <option value="Licitación Pública">Licitación Pública</option>
                                                <option value="Concurso Público">Concurso Público</option>
                                                <option value="Adjudicación Simplificada">Adjudicación Simplificada</option>
                                                <option value="Selección de Consultores Individuales">Selección de Consultores Individuales</option>
                                                <option value="Comparación de Precios">Comparación de Precios</option>
                                                <option value="Subasta Inversa Electrónica">Subasta Inversa Electrónica</option>
                                                <option value="Contratación Directa">Contratación Directa</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Estado Proceso *</label>
                                            <select
                                                required
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.estado_proceso || 'CONVOCADO'}
                                                onChange={(e) => handleChange("estado_proceso", e.target.value)}
                                            >
                                                <option value="ADJUDICADO">ADJUDICADO</option>
                                                <option value="APELADO">APELADO</option>
                                                <option value="BLOQUEADO">BLOQUEADO</option>
                                                <option value="CANCELADO">CANCELADO</option>
                                                <option value="CONSENTIDO">CONSENTIDO</option>
                                                <option value="CONTRATADO">CONTRATADO</option>
                                                <option value="CONVOCADO">CONVOCADO</option>
                                                <option value="CONVOCADO_POR_REINICIO">CONVOCADO_POR_REINICIO</option>
                                                <option value="DESIERTO">DESIERTO</option>
                                                <option value="NO_SUSCRIPCION_CONTRATO POR_DECISION_ENTIDAD">NO_SUSCRIPCION_CONTRATO POR_DECISION_ENTIDAD</option>
                                                <option value="NULO">NULO</option>
                                                <option value="PENDIENTE_DE_REGISTRO_DE_EFECTO">PENDIENTE_DE_REGISTRO_DE_EFECTO</option>
                                                <option value="RETROTRAIDO_POR_RESOLUCION">RETROTRAIDO_POR_RESOLUCION</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Categoría *</label>
                                            <select
                                                required
                                                className="w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                value={formData.categoria || ''}
                                                onChange={(e) => handleChange("categoria", e.target.value)}
                                            >
                                                <option value="">Seleccionar...</option>
                                                <option value="BIENES">BIENES</option>
                                                <option value="SERVICIOS">SERVICIOS</option>
                                                <option value="OBRAS">OBRAS</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Monto Estimado</label>
                                            <div className="flex gap-2">
                                                <select
                                                    className="w-24 rounded-lg border border-gray-300 px-2 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                    value={formData.moneda || 'PEN'}
                                                    onChange={(e) => handleChange("moneda", e.target.value)}
                                                >
                                                    <option value="PEN">PEN</option>
                                                    <option value="USD">USD</option>
                                                </select>
                                                <input
                                                    type="number"
                                                    step="0.01"
                                                    className="flex-1 rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                    value={formData.monto_estimado || 0}
                                                    onChange={(e) => handleChange("monto_estimado", parseFloat(e.target.value))}
                                                />
                                            </div>
                                        </div>

                                        <div>
                                            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Fechas Generales</label>
                                            <div className="grid grid-cols-2 gap-2">
                                                <div className="flex flex-col">
                                                    <span className="text-xs text-gray-500 mb-1">Publicación</span>
                                                    <input
                                                        type="date"
                                                        className="rounded-lg border border-gray-300 px-2 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                        value={formData.fecha_publicacion ? formData.fecha_publicacion.split('T')[0] : ''}
                                                        onChange={(e) => handleChange("fecha_publicacion", e.target.value)}
                                                    />
                                                </div>
                                                <div className="flex flex-col">
                                                    <span className="text-xs text-gray-500 mb-1">Adjudicación (Est.)</span>
                                                    <input
                                                        type="date"
                                                        className="rounded-lg border border-gray-300 px-2 py-2 dark:border-gray-700 dark:bg-gray-800"
                                                        value={formData.fecha_adjudicacion ? formData.fecha_adjudicacion.split('T')[0] : ''}
                                                        onChange={(e) => handleChange("fecha_adjudicacion", e.target.value)}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {/* TAB 2: ADJUDICACIONES */}
                                {activeTab === "adjudicaciones" && (
                                    <div className="space-y-6">
                                        {formData.adjudicaciones?.map((adj, index) => (
                                            <div key={index} className="rounded-xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800/50">
                                                {/* Header Adjudicacion */}
                                                <div className="mb-4 flex items-center justify-between">
                                                    <h4 className="font-semibold text-gray-800 dark:text-gray-200">
                                                        Adjudicación #{index + 1}
                                                    </h4>
                                                    <button
                                                        type="button"
                                                        onClick={() => removeAdjudicacion(index)}
                                                        className="text-red-500 hover:text-red-700 font-medium text-sm"
                                                    >
                                                        Eliminar Item
                                                    </button>
                                                </div>

                                                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">Ganador</label>
                                                        <input
                                                            type="text"
                                                            placeholder="Ej: CONSTRUCTORA DEL SUR S.A.C."
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.ganador_nombre || ''}
                                                            onChange={(e) => updateAdjudicacion(index, "ganador_nombre", e.target.value)}
                                                        />
                                                    </div>
                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">RUC</label>
                                                        <input
                                                            type="text"
                                                            placeholder="Ej: 20601234567"
                                                            maxLength={11}
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.ganador_ruc || ''}
                                                            onChange={(e) => updateAdjudicacion(index, "ganador_ruc", e.target.value)}
                                                        />
                                                    </div>
                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">Monto Adjudicado</label>
                                                        <input
                                                            type="number"
                                                            step="0.01"
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.monto_adjudicado || 0}
                                                            onChange={(e) => updateAdjudicacion(index, "monto_adjudicado", parseFloat(e.target.value))}
                                                        />
                                                    </div>

                                                    {/* New Fields per Item */}
                                                    {/* Constants defined above component or inside if preferred, but for replacement simplicity I will inline options or use a helper array if possible, but replace_content is chunk-based. */}
                                                    {/* actually, I will add the constants at the top of the file in a separate call if needed, but for now I will hardcode the options in the JSX for simplicity as requested by "replace inputs" */}

                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">Fecha Adjudicación (Item)</label>
                                                        <input
                                                            type="date"
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.fecha_adjudicacion ? (typeof adj.fecha_adjudicacion === 'string' ? adj.fecha_adjudicacion.split('T')[0] : '') : ''}
                                                            onChange={(e) => updateAdjudicacion(index, "fecha_adjudicacion", e.target.value)}
                                                        />
                                                    </div>
                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">Estado Item</label>
                                                        <select
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.estado_item || "ADJUDICADO"}
                                                            onChange={(e) => updateAdjudicacion(index, "estado_item", e.target.value)}
                                                        >
                                                            <option value="ADJUDICADO">ADJUDICADO</option>
                                                            <option value="CONSENTIDO">CONSENTIDO</option>
                                                            <option value="CONTRATADO">CONTRATADO</option>
                                                            <option value="DESIERTO">DESIERTO</option>
                                                            <option value="CANCELADO">CANCELADO</option>
                                                            <option value="ANULADO">ANULADO</option>
                                                        </select>
                                                    </div>
                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">Tipo Garantía</label>
                                                        <select
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.tipo_garantia || ''}
                                                            onChange={(e) => updateAdjudicacion(index, "tipo_garantia", e.target.value)}
                                                        >
                                                            <option value="">Seleccionar...</option>
                                                            <option value="GARANTIA_BANCARIA">GARANTIA_BANCARIA</option>
                                                            <option value="RETENCION">RETENCION</option>
                                                        </select>
                                                    </div>

                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">ID Contrato (Opcional)</label>
                                                        <input
                                                            type="text"
                                                            placeholder="Ej: CTR-001-2024"
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.id_contrato || ''}
                                                            onChange={(e) => updateAdjudicacion(index, "id_contrato", e.target.value)}
                                                        />
                                                    </div>
                                                    <div>
                                                        <label className="text-xs font-medium text-gray-500">Garantía / Banco</label>
                                                        <input
                                                            list={`entidades-list-${index}`}
                                                            type="text"
                                                            placeholder="Ej: BCP"
                                                            className="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm dark:border-gray-600 dark:bg-gray-700"
                                                            value={adj.entidad_financiera || ''}
                                                            onChange={(e) => updateAdjudicacion(index, "entidad_financiera", e.target.value)}
                                                        />
                                                        <datalist id={`entidades-list-${index}`}>
                                                            <option value="AVLA PERU COMPAÑIA DE SEGUROS S A" />
                                                            <option value="SECREX CESCE S.A. COMPAÑIA DE SEGUROS Y REASEGUROS" />
                                                            <option value="CRECER SEGUROS S.A. COMPAÑÍA DE SEGUROS" />
                                                            <option value="INSUR S.A. COMPAÑIA DE SEGUROS" />
                                                            <option value="MAPFRE PERU COMPAÑIA DE SEGUROS Y REASEGUROS" />
                                                            <option value="ECA SEGUROS S.A. (EN LIQUIDACION)" />
                                                            <option value="LIBERTY SEGUROS S.A." />
                                                            <option value="CESCE PERÚ S.A. COMPAÑIA DE SEGUROS" />
                                                            <option value="BANCO DE CREDITO DEL PERU" />
                                                            <option value="BBVA PERÚ" />
                                                            <option value="BANCO INTERNACIONAL DEL PERU - INTERBANK" />
                                                            <option value="SCOTIABANK PERU S.A.A." />
                                                            <option value="BANCO PICHINCHA" />
                                                            <option value="BANCO BIF" />
                                                            <option value="BANCO SANTANDER PERU S.A." />
                                                            <option value="CMAC HUANCAYO" />
                                                            <option value="CMAC AREQUIPA" />
                                                            <option value="CMAC CUSCO S A" />
                                                            <option value="CMAC PIURA" />
                                                            <option value="CMAC TRUJILLO" />
                                                            <option value="COOPERATIVA DE AHORRO Y CREDITO PACIFICO" />
                                                            <option value="LA POSITIVA SEGUROS Y REASEGUROS" />
                                                            <option value="RIMAC SEGUROS Y REASEGUROS" />
                                                            <option value="CHUBB PERU S.A. COMPAÑIA DE SEGUROS Y REASEGUROS" />
                                                            <option value="PROTECTA S.A. COMPAÑIA DE SEGUROS" />
                                                            <option value="CARDIF DEL PERU S.A. COMPAÑIA DE SEGUROS" />
                                                            <option value="RIGEL PERU S.A. COMPAÑIA DE SEGUROS DE VIDA" />
                                                            <option value="OH!! S.A." />
                                                        </datalist>
                                                    </div>
                                                </div>

                                                {/* Consorcios Section */}
                                                <div className="mt-4 border-t border-gray-200 pt-3 dark:border-gray-700">
                                                    <div className="flex items-center justify-between mb-2">
                                                        <label className="text-xs font-bold uppercase tracking-wider text-gray-500">
                                                            Miembros del Consorcio (Si aplica)
                                                        </label>
                                                        <button
                                                            type="button"
                                                            onClick={() => addConsorcioMember(index)}
                                                            className="text-xs text-blue-600 hover:underline"
                                                        >
                                                            + Agregar Miembro
                                                        </button>
                                                    </div>

                                                    {/* Header for Consorcio Members */}
                                                    {(adj.consorcios && adj.consorcios.length > 0) && (
                                                        <div className="flex gap-2 mb-1 px-1">
                                                            <span className="flex-1 text-[10px] uppercase text-gray-500 font-semibold">Nombre del Socio</span>
                                                            <span className="w-24 text-[10px] uppercase text-gray-500 font-semibold">RUC</span>
                                                            <span className="w-16 text-[10px] uppercase text-gray-500 font-semibold text-center">% Part.</span>
                                                            <span className="w-5"></span>
                                                        </div>
                                                    )}

                                                    {adj.consorcios?.map((member, mIndex) => (
                                                        <div key={mIndex} className="mb-2 flex items-center gap-2">
                                                            <input
                                                                type="text"
                                                                placeholder="Nombre Completo del Socio"
                                                                className="flex-1 rounded border border-gray-300 px-2 py-1 text-xs dark:border-gray-600 dark:bg-gray-700"
                                                                value={member.nombre_miembro}
                                                                onChange={(e) => updateConsorcioMember(index, mIndex, "nombre_miembro", e.target.value)}
                                                            />
                                                            <input
                                                                type="text"
                                                                placeholder="RUC"
                                                                maxLength={11}
                                                                className="w-24 rounded border border-gray-300 px-2 py-1 text-xs dark:border-gray-600 dark:bg-gray-700"
                                                                value={member.ruc_miembro}
                                                                onChange={(e) => updateConsorcioMember(index, mIndex, "ruc_miembro", e.target.value)}
                                                            />
                                                            <input
                                                                type="number"
                                                                placeholder="%"
                                                                className="w-16 rounded border border-gray-300 px-2 py-1 text-xs text-center dark:border-gray-600 dark:bg-gray-700"
                                                                value={member.porcentaje_participacion}
                                                                onChange={(e) => updateConsorcioMember(index, mIndex, "porcentaje_participacion", parseFloat(e.target.value))}
                                                            />
                                                            <button
                                                                type="button"
                                                                onClick={() => removeConsorcioMember(index, mIndex)}
                                                                className="text-gray-400 hover:text-red-500"
                                                            >
                                                                ✕
                                                            </button>
                                                        </div>
                                                    ))}
                                                    {(!adj.consorcios || adj.consorcios.length === 0) && (
                                                        <p className="text-xs italic text-gray-400">Sin miembros registrados.</p>
                                                    )}
                                                </div>
                                            </div>
                                        ))}

                                        <button
                                            type="button"
                                            onClick={addAdjudicacion}
                                            className="flex w-full items-center justify-center rounded-xl border-2 border-dashed border-gray-300 py-3 font-semibold text-gray-500 transition-colors hover:border-blue-500 hover:bg-blue-50 hover:text-blue-600 dark:border-gray-600 dark:hover:bg-gray-800"
                                        >
                                            + Agregar Adjudicación
                                        </button>
                                    </div>
                                )}
                            </form>
                        )}
                    </div>

                    {/* Footer */}
                    <div className="flex justify-end gap-3 border-t border-gray-200 px-6 py-4 dark:border-gray-700 shrink-0">
                        <button
                            type="button"
                            onClick={onClose}
                            className="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
                        >
                            Cancelar
                        </button>
                        <button
                            onClick={handleSubmit} // Trigger external submit
                            disabled={isSaving}
                            className="rounded-lg bg-blue-600 px-6 py-2 text-sm font-medium text-white shadow-lg shadow-blue-500/30 transition-all hover:bg-blue-700 hover:shadow-blue-500/40 disabled:opacity-50"
                        >
                            {isSaving ? "Guardando..." : "Guardar Licitación"}
                        </button>
                    </div>

                </div>
            </div>
        </div>
    );
};
