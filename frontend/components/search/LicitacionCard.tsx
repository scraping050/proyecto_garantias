import React from "react";
import Link from "next/link";
import {
    FileText,
    Building2,
    MapPin,
    Tag,
    DollarSign,
    Calendar,
    FileCode,
    ShieldCheck,
    Eye,
    Download
} from "lucide-react";
import type { Licitacion } from "@/types/licitacion";

interface Props {
    licitacion: Licitacion;
}

export const LicitacionCard: React.FC<Props> = ({ licitacion }) => {

    const formatDate = (dateString: string) => {
        if (!dateString) return "N/A";
        return new Date(dateString).toLocaleDateString("es-PE", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        });
    };

    const formatCurrency = (amount?: number, currency: string = "PEN") => {
        if (amount === undefined || amount === null) return "S/ 0.00";
        return new Intl.NumberFormat("es-PE", {
            style: "currency",
            currency: currency || "PEN",
        }).format(amount);
    };

    // Helper for Status Badge Color (Yellow background as per image reference for "CONVOCADO")
    const getStatusStyles = (status?: string) => {
        const s = status?.toUpperCase() || "";
        if (s.includes("CONVOCADO")) return "bg-[#FFF9C4] text-[#8D6E1F] border border-[#FDE047]"; // Yellow-ish
        if (s.includes("ADJUDICADO")) return "bg-emerald-100 text-emerald-700 border border-emerald-200";
        if (s.includes("DESIERTO")) return "bg-red-100 text-red-700 border border-red-200";
        return "bg-slate-100 text-slate-700 border border-slate-200";
    };

    return (
        <div className="flex flex-col justify-between overflow-hidden rounded-3xl bg-white p-6 shadow-sm border border-slate-100 transition-all hover:shadow-md dark:bg-[#111c44] dark:border-white/5 h-full">

            {/* Header Section */}
            <div className="flex items-start gap-4 mb-4">
                {/* Icon Box */}
                <div className="shrink-0">
                    <div className="w-12 h-12 rounded-xl bg-[#EEF2FF] flex items-center justify-center dark:bg-indigo-500/20">
                        <FileText className="w-6 h-6 text-[#6366F1] dark:text-indigo-400" />
                    </div>
                </div>

                {/* Nomenclatura & OCID & Status */}
                <div className="flex-1 min-w-0">
                    <div className="flex flex-col gap-2">
                        <div className="flex items-start justify-between gap-2">
                            <h4 className="font-bold text-slate-900 text-sm break-words dark:text-white" title={licitacion.nomenclatura}>
                                {licitacion.nomenclatura || "SIN NOMENCLATURA"}
                            </h4>
                            <span className={`shrink-0 px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wide whitespace-nowrap ${getStatusStyles(licitacion.estado_proceso)}`}>
                                {licitacion.estado_proceso || "PENDIENTE"}
                            </span>
                        </div>
                        <p className="text-[10px] text-slate-400 break-all" title={licitacion.ocid}>
                            {licitacion.ocid || `ocds-id-${licitacion.id_convocatoria}`}
                        </p>
                    </div>
                </div>
            </div>

            {/* Title */}
            <h3 className="text-sm font-extrabold text-[#0F172A] uppercase leading-tight mb-6 dark:text-white">
                {licitacion.descripcion}
            </h3>

            {/* Details Grid */}
            <div className="space-y-4 mb-6">

                {/* Comprador */}
                <div className="flex items-start gap-3">
                    <Building2 className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium">Comprador</p>
                        <p className="text-xs font-bold text-slate-700 uppercase break-words dark:text-slate-200">
                            {licitacion.comprador || "ENTIDAD DESCONOCIDA"}
                        </p>
                    </div>
                </div>

                {/* Ubicación */}
                <div className="flex items-start gap-3">
                    <MapPin className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium">Ubicación</p>
                        <p className="text-xs font-bold text-slate-700 uppercase break-words dark:text-slate-200">
                            {licitacion.departamento || "LIMA"} - {licitacion.provincia || "LIMA"} - {licitacion.distrito || "LIMA"}
                        </p>
                    </div>
                </div>

                {/* Categoría */}
                <div className="flex items-start gap-3">
                    <Tag className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium mb-1">Categoría</p>
                        <div className="flex flex-wrap gap-2">
                            <span className="px-2 py-0.5 rounded-md bg-purple-100 text-purple-700 text-[10px] font-bold uppercase dark:bg-purple-900/30 dark:text-purple-300">
                                {licitacion.categoria || "BIENES"}
                            </span>
                            <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-[10px] font-medium dark:bg-slate-700/50 dark:text-slate-300">
                                Licitación Pública
                            </span>
                        </div>
                    </div>
                </div>

                {/* Monto */}
                <div className="flex items-start gap-3">
                    <DollarSign className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium">Monto Estimado</p>
                        <p className="text-lg font-bold text-[#4F46E5] dark:text-[#6366f1]">
                            {formatCurrency(licitacion.monto_estimado, licitacion.moneda)}
                        </p>
                    </div>
                </div>

                {/* Fecha */}
                <div className="flex items-start gap-3">
                    <Calendar className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium">Fecha de Publicación</p>
                        <p className="text-xs font-bold text-slate-700 dark:text-slate-200">
                            {formatDate(licitacion.fecha_publicacion)}
                        </p>
                    </div>
                </div>

                {/* Identificadores */}
                <div className="flex items-start gap-3">
                    <FileCode className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium">Identificadores</p>
                        <p className="text-xs font-bold text-blue-600 dark:text-blue-400 cursor-pointer break-all">
                            Conv: {licitacion.id_convocatoria || "N/A"}
                        </p>
                    </div>
                </div>

                {/* Adjudicaciones */}
                <div className="flex items-start gap-3">
                    <ShieldCheck className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
                    <div className="min-w-0 flex-1">
                        <p className="text-xs text-slate-400 font-medium">Adjudicaciones</p>
                        <p className="text-xs font-bold text-emerald-600 dark:text-emerald-400">
                            0 • Con garantía: 0
                        </p>
                    </div>
                </div>
            </div>

            {/* Footer Buttons */}
            <div className="mt-auto flex flex-col sm:flex-row gap-3 pt-4 border-t border-slate-100 dark:border-white/5">
                <div
                    className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-[#4F46E5] py-2.5 text-sm font-bold text-white shadow-sm shadow-indigo-500/20 cursor-default"
                >
                    <Eye className="w-4 h-4" />
                    Ver Detalles
                </div>
                <div
                    className="flex-1 flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-bold text-slate-700 dark:bg-[#0b122b] dark:border-slate-700 dark:text-white cursor-default"
                >
                    <Download className="w-4 h-4" />
                    Descargar
                </div>
            </div>
        </div>
    );
};
