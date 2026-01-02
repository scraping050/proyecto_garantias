"use client";
import React from "react";
import PageBreadcrumb from "@/components/common/PageBreadCrumb";
import LicitacionForm from "@/components/gestion-manual/LicitacionForm";

export default function NuevaLicitacionPage() {
    return (
        <div>
            <PageBreadcrumb pageTitle="Nueva Licitación" />
            <div className="max-w-7xl mx-auto">
                <LicitacionForm />
            </div>
        </div>
    );
}
