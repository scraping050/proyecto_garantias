"use client";
import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import PageBreadcrumb from "@/components/common/PageBreadCrumb";
import LicitacionForm from "@/components/gestion-manual/LicitacionForm";
import { Licitacion } from "@/types/licitacion";

export default function EditarLicitacionClient() {
    const params = useParams();
    const id = params.id;
    const [licitacion, setLicitacion] = useState<Licitacion | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!id) return;

        const fetchLicitacion = async () => {
            try {
                // Determine API URL for production vs dev
                const apiUrl = process.env.NEXT_PUBLIC_BASE_URL ? `${process.env.NEXT_PUBLIC_BASE_URL}/api` : '/api';
                // Wait, SEACE rewrite uses /api internally?
                // The original code used /api/gestion-manual...
                // NEXT_PUBLIC_API_URL is https://seace-api...
                // But original code uses relative path /api.
                // In static export, usage of /api relative path assumes the backend is on same domain or handled by rewrite?
                // Rewrite DOES NOT WORK in static export.
                // So fetch('/api/...') will fetch from current domain (mcqs-jcq.com/api/...).
                // If API is on api.mcqs-jcq.com, we MUST use absolute URL.

                // I should update this to use NEXT_PUBLIC_API_URL.
                const baseUrl = process.env.NEXT_PUBLIC_API_URL || '';
                const res = await fetch(`${baseUrl}/gestion-manual/licitaciones/${id}`);
                const data = await res.json();
                if (data.success) {
                    setLicitacion(data.data);
                }
            } catch (error) {
                console.error(error);
                alert("Error al cargar datos");
            } finally {
                setLoading(false);
            }
        };

        fetchLicitacion();
    }, [id]);

    if (loading) return <div>Cargando...</div>;
    if (!licitacion) return <div>No encontrada</div>;

    return (
        <div>
            <PageBreadcrumb pageTitle="Editar Licitación" />
            <div className="max-w-7xl mx-auto">
                <LicitacionForm initialData={licitacion} isEditing={true} />
            </div>
        </div>
    );
}
