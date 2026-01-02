"use client";
import React, { useEffect, useState } from "react";
import { ArrowDownIcon, ArrowUpIcon, BoxIconLine, GroupIcon } from "@/icons";

interface MetricsData {
    total_licitaciones: number;
    monto_total_adjudicado: string;
}

// Helper function to format currency
const formatCurrency = (amount: any): string => {
    // Safely convert to number
    const numericValue = typeof amount === 'number' ? amount : parseFloat(String(amount || '0'));

    if (isNaN(numericValue)) return 'S/ 0.00';

    // Format with thousand separators and 2 decimals
    return `S/ ${numericValue.toLocaleString('es-PE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const EcommerceMetrics = () => {
    const [metrics, setMetrics] = useState<MetricsData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/reportes/resumen-ejecutivo`);
                const data = await response.json();

                if (data.success) {
                    setMetrics({
                        total_licitaciones: data.data.total_licitaciones,
                        monto_total_adjudicado: data.data.monto_total
                    });
                }
            } catch (error) {
                console.error('Error fetching metrics:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchMetrics();
    }, []);

    return (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-6">
            {/* <!-- Metric Item Start --> */}
            <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6">
                <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-xl dark:bg-gray-800">
                    <GroupIcon className="text-gray-800 size-6 dark:text-white/90" />
                </div>

                <div className="mt-5">
                    <div>
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                            Licitaciones
                        </span>
                        <h4 className="mt-2 font-bold text-gray-800 text-title-sm dark:text-white/90">
                            {loading ? '...' : metrics?.total_licitaciones.toLocaleString() || '0'}
                        </h4>
                    </div>
                </div>
            </div>
            {/* <!-- Metric Item End --> */}

            {/* <!-- Metric Item Start --> */}
            <div className="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] md:p-6">
                <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-xl dark:bg-gray-800">
                    <BoxIconLine className="text-gray-800 dark:text-white/90" />
                </div>
                <div className="mt-5">
                    <div>
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                            Monto Adjudicado
                        </span>
                        <h4 className="mt-2 font-bold text-gray-800 text-title-sm dark:text-white/90">
                            {loading ? '...' : (metrics?.monto_total_adjudicado ? formatCurrency(metrics.monto_total_adjudicado) : 'S/ 0.00')}
                        </h4>
                    </div>
                </div>
            </div>
            {/* <!-- Metric Item End --> */}
        </div>
    );
};
