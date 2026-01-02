"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Licitacion } from "@/types/licitacion";
import ComponentCard from "@/components/common/ComponentCard";
import Label from "@/components/form/Label";
import Input from "@/components/form/input/InputField";
import Select from "@/components/form/Select";
import { ChevronDownIcon, CalendarIcon, DollarLineIcon } from "@/icons";

interface LicitacionFormProps {
    initialData?: Partial<Licitacion> & { adjudicaciones?: any[] };
    isEditing?: boolean;
}

export default function LicitacionForm({ initialData, isEditing = false }: LicitacionFormProps) {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<Partial<Licitacion>>({
        nomenclatura: "",
        descripcion: "",
        comprador: "",
        categoria: "Bienes",
        departamento: "",
        provincia: "",
        distrito: "",
        monto_estimado: 0,
        moneda: "PEN",
        fecha_publicacion: new Date().toISOString().split("T")[0],
        estado_proceso: "CONVOCADO",
        tipo_procedimiento: "",
        ...initialData
    });

    // Garantias State
    const [adjudicaciones, setAdjudicaciones] = useState<any[]>(initialData?.adjudicaciones || []);
    const [newGarantia, setNewGarantia] = useState({
        ganador_nombre: "",
        ganador_ruc: "",
        monto_adjudicado: 0,
        entidad_financiera: "",
        tipo_garantia: "CARTA FIANZA"
    });
    const [showGarantiaForm, setShowGarantiaForm] = useState(false);

    const handleAddGarantia = () => {
        if (!newGarantia.ganador_nombre || !newGarantia.monto_adjudicado) {
            alert("Por favor complete el nombre del ganador y el monto.");
            return;
        }
        setAdjudicaciones([...adjudicaciones, { ...newGarantia, id_temp: Date.now() }]);
        setNewGarantia({
            ganador_nombre: "",
            ganador_ruc: "",
            monto_adjudicado: 0,
            entidad_financiera: "",
            tipo_garantia: "CARTA FIANZA"
        });
        setShowGarantiaForm(false);
    };

    const removeGarantia = (index: number) => {
        const newAdj = [...adjudicaciones];
        newAdj.splice(index, 1);
        setAdjudicaciones(newAdj);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSelectChange = (name: string, value: string) => {
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const url = isEditing
                ? `/api/gestion-manual/licitaciones/${initialData?.id_convocatoria}`
                : "/api/gestion-manual/licitaciones";

            const method = isEditing ? "PUT" : "POST";

            const res = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ...formData, adjudicaciones }),
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.message || "Error al guardar");

            router.push("/gestion-manual");
            router.refresh();
        } catch (error: any) {
            console.error(error);
            alert(`Error: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const categoryOptions = [
        { value: "Bienes", label: "Bienes" },
        { value: "Servicios", label: "Servicios" },
        { value: "Obras", label: "Obras" },
        { value: "Consultoría de Obras", label: "Consultoría de Obras" },
    ];

    const currencyOptions = [
        { value: "PEN", label: "PEN" },
        { value: "USD", label: "USD" },
        { value: "EUR", label: "EUR" },
    ];

    return (
        <div className="grid grid-cols-1 gap-9 sm:grid-cols-2">
            <div className="flex flex-col gap-9">
                {/* Datos Principales */}
                <ComponentCard title="Datos Principales">
                    <div className="space-y-6">
                        <div>
                            <Label>Nomenclatura *</Label>
                            <Input
                                type="text"
                                name="nomenclatura"
                                defaultValue={formData.nomenclatura}
                                onChange={handleChange}
                                placeholder="Ej: LP-SM-12-2025-MINSA"
                            />
                        </div>

                        <div>
                            <Label>Descripción *</Label>
                            <div className="relative">
                                <textarea
                                    name="descripcion"
                                    rows={4}
                                    value={formData.descripcion}
                                    onChange={handleChange}
                                    placeholder="Descripción detallada..."
                                    className="w-full rounded-lg border border-gray-300 bg-transparent px-4 py-3 text-black outline-none transition focus:border-brand-500 active:border-brand-500 disabled:cursor-default disabled:bg-gray-200 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500"
                                ></textarea>
                            </div>
                        </div>

                        <div>
                            <Label>Comprador (Entidad)</Label>
                            <Input
                                type="text"
                                name="comprador"
                                defaultValue={formData.comprador}
                                onChange={handleChange}
                                placeholder="Ej: MINISTERIO DE SALUD"
                            />
                        </div>
                    </div>
                </ComponentCard>

                <ComponentCard title="Detalles del Proceso">
                    <div className="space-y-6">
                        <div>
                            <Label>Categoría</Label>
                            <div className="relative">
                                <Select
                                    options={categoryOptions}
                                    defaultValue={formData.categoria}
                                    placeholder="Seleccionar Categoría"
                                    onChange={(val) => handleSelectChange('categoria', val)}
                                // className="dark:bg-dark-900" 
                                // Select component implementation might vary, passing props carefully
                                />
                                <span className="absolute text-gray-500 -translate-y-1/2 pointer-events-none right-3 top-1/2 dark:text-gray-400">
                                    <ChevronDownIcon />
                                </span>
                            </div>
                        </div>

                        <div>
                            <Label>Estado del Proceso</Label>
                            <Input
                                type="text"
                                name="estado_proceso"
                                defaultValue={formData.estado_proceso}
                                onChange={handleChange}
                                placeholder="Ej: CONVOCADO"
                            />
                        </div>
                    </div>
                </ComponentCard>
            </div>

            <div className="flex flex-col gap-9">
                {/* Ubicación y Económicos */}
                <ComponentCard title="Ubicación Geográfica">
                    <div className="space-y-6">
                        <div>
                            <Label>Departamento</Label>
                            <Input
                                type="text"
                                name="departamento"
                                defaultValue={formData.departamento}
                                onChange={handleChange}
                                placeholder="Ej: LIMA"
                            />
                        </div>
                        <div>
                            <Label>Provincia</Label>
                            <Input
                                type="text"
                                name="provincia"
                                defaultValue={formData.provincia}
                                onChange={handleChange}
                                placeholder="Ej: LIMA"
                            />
                        </div>
                        <div>
                            <Label>Distrito</Label>
                            <Input
                                type="text"
                                name="distrito"
                                defaultValue={formData.distrito}
                                onChange={handleChange}
                                placeholder="Ej: MIRAFLORES"
                            />
                        </div>
                    </div>
                </ComponentCard>

                <ComponentCard title="Datos Económicos y Fechas">
                    <div className="space-y-6">
                        <div>
                            <Label>Monto Estimado</Label>
                            <div className="relative">
                                <Input
                                    type="number"
                                    name="monto_estimado"
                                    defaultValue={formData.monto_estimado}
                                    onChange={handleChange}
                                    placeholder="0.00"
                                    className="pl-[62px]" // Space for icon
                                />
                                <span className="absolute left-0 top-1/2 flex h-11 w-[46px] -translate-y-1/2 items-center justify-center border-r border-gray-200 dark:border-gray-800">
                                    <DollarLineIcon className="fill-gray-500 dark:fill-gray-400" />
                                </span>
                            </div>
                        </div>

                        <div>
                            <Label>Moneda</Label>
                            <div className="relative">
                                <Select
                                    options={currencyOptions}
                                    defaultValue={formData.moneda}
                                    placeholder="Seleccionar Moneda"
                                    onChange={(val) => handleSelectChange('moneda', val)}
                                />
                                <span className="absolute text-gray-500 -translate-y-1/2 pointer-events-none right-3 top-1/2 dark:text-gray-400">
                                    <ChevronDownIcon />
                                </span>
                            </div>
                        </div>

                        <div>
                            <Label>Fecha Publicación</Label>
                            <Input
                                type="date"
                                name="fecha_publicacion"
                                defaultValue={formData.fecha_publicacion ? new Date(formData.fecha_publicacion).toISOString().split('T')[0] : ''}
                                onChange={handleChange}
                            />
                        </div>
                    </div>
                </ComponentCard>

                {/* Section: Garantías y Adjudicaciones */}
                <ComponentCard title="Garantías y Adjudicaciones">
                    <div className="space-y-4">
                        {/* List of existing guarantees */}
                        {adjudicaciones.length > 0 && (
                            <div className="rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                    <thead className="bg-gray-50 dark:bg-gray-800">
                                        <tr>
                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ganador</th>
                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto Adj.</th>
                                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Banco / Garantía</th>
                                            <th className="px-4 py-3 relative"><span className="sr-only">Actions</span></th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
                                        {adjudicaciones.map((adj, idx) => (
                                            <tr key={idx}>
                                                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                                    {adj.ganador_nombre} <br /> <span className="text-xs text-gray-500">{adj.ganador_ruc}</span>
                                                </td>
                                                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                                    {adj.moneda || 'S/'} {Number(adj.monto_adjudicado).toFixed(2)}
                                                </td>
                                                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                                    {adj.entidad_financiera} <br /> <span className="text-xs text-brand-500">{adj.tipo_garantia}</span>
                                                </td>
                                                <td className="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
                                                    <button
                                                        onClick={() => removeGarantia(idx)}
                                                        type="button"
                                                        className="text-red-600 hover:text-red-900"
                                                    >
                                                        Eliminar
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}

                        {/* Add New Button/Form */}
                        {!showGarantiaForm ? (
                            <button
                                type="button"
                                onClick={() => setShowGarantiaForm(true)}
                                className="flex items-center text-primary font-medium hover:underline"
                            >
                                + Agregar Garantía / Adjudicación
                            </button>
                        ) : (
                            <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 space-y-4">
                                <h4 className="font-medium text-gray-900 dark:text-white text-sm">Nueva Adjudicación</h4>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    <div>
                                        <Label>Ganador (Nombre/Razón Social)</Label>
                                        <Input
                                            defaultValue={newGarantia.ganador_nombre}
                                            onChange={(e) => setNewGarantia({ ...newGarantia, ganador_nombre: e.target.value })}
                                            placeholder="CONSORCIO EJEMPLO"
                                        />
                                    </div>
                                    <div>
                                        <Label>RUC Ganador</Label>
                                        <Input
                                            defaultValue={newGarantia.ganador_ruc}
                                            onChange={(e) => setNewGarantia({ ...newGarantia, ganador_ruc: e.target.value })}
                                            placeholder="201000..."
                                        />
                                    </div>
                                    <div>
                                        <Label>Monto Adjudicado</Label>
                                        <Input
                                            type="number"
                                            defaultValue={newGarantia.monto_adjudicado}
                                            onChange={(e) => setNewGarantia({ ...newGarantia, monto_adjudicado: parseFloat(e.target.value) })}
                                            placeholder="0.00"
                                        />
                                    </div>
                                    <div>
                                        <Label>Entidad Financiera (Garantía)</Label>
                                        <Input
                                            defaultValue={newGarantia.entidad_financiera}
                                            onChange={(e) => setNewGarantia({ ...newGarantia, entidad_financiera: e.target.value })}
                                            placeholder="BBVA, BCP, ETC."
                                        />
                                    </div>
                                </div>
                                <div className="flex justify-end gap-3 mt-2">
                                    <button
                                        type="button"
                                        onClick={() => setShowGarantiaForm(false)}
                                        className="px-4 py-2 text-sm text-gray-600 bg-white border border-gray-300 rounded hover:bg-gray-50"
                                    >
                                        Cancelar
                                    </button>
                                    <button
                                        type="button"
                                        onClick={handleAddGarantia}
                                        className="px-4 py-2 text-sm text-white bg-primary rounded hover:bg-opacity-90"
                                    >
                                        Agregar a la lista
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </ComponentCard>

                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="flex w-full justify-center rounded-lg bg-primary p-3 font-medium text-white hover:bg-opacity-90 disabled:opacity-50"
                >
                    {loading ? "Guardando..." : isEditing ? "Actualizar Licitación" : "Crear Licitación"}
                </button>
            </div>
        </div>
    );
}
