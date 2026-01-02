"use client";
import { ApexOptions } from "apexcharts";
import dynamic from "next/dynamic";
import { Dropdown } from "../ui/dropdown/Dropdown";
import { MoreDotIcon } from "@/icons";
import { useState, useEffect } from "react";
import { DropdownItem } from "../ui/dropdown/DropdownItem";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
    ssr: false,
});

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

interface CategoriaData {
    bien: number;
    servicio: number;
    obra: number;
    total: number;
}

export default function MonthlyTarget() {
    const [categoriaData, setCategoriaData] = useState<CategoriaData>({
        bien: 0,
        servicio: 0,
        obra: 0,
        total: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCategoriaData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/reportes/por-categoria`);
                const data = await response.json();

                if (data.success && data.data && data.data.categorias) {
                    const bien = data.data.categorias.find((cat: any) => cat.categoria === 'BIENES')?.total || 0;
                    const servicio = data.data.categorias.find((cat: any) => cat.categoria === 'SERVICIOS')?.total || 0;
                    const obra = data.data.categorias.find((cat: any) => cat.categoria === 'OBRAS')?.total || 0;
                    const total = bien + servicio + obra;

                    setCategoriaData({
                        bien,
                        servicio,
                        obra,
                        total
                    });
                }
            } catch (error) {
                console.error('Error fetching categoria data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchCategoriaData();
    }, []);

    const porcentajeBien = categoriaData.total > 0 ? (categoriaData.bien / categoriaData.total * 100) : 0;
    const porcentajeServicio = categoriaData.total > 0 ? (categoriaData.servicio / categoriaData.total * 100) : 0;
    const porcentajeObra = categoriaData.total > 0 ? (categoriaData.obra / categoriaData.total * 100) : 0;

    const chartSeries: number[] = [porcentajeBien, porcentajeServicio, porcentajeObra];
    const chartLabels: string[] = ['Bien', 'Servicio', 'Obra'];
    const chartColors: string[] = ['#465FFF', '#10B981', '#F59E0B'];

    const options: ApexOptions = {
        colors: chartColors,
        chart: {
            fontFamily: "Outfit, sans-serif",
            type: "radialBar",
            height: 280,
        },
        plotOptions: {
            radialBar: {
                startAngle: -90,
                endAngle: 90,
                hollow: {
                    size: "70%",
                },
                track: {
                    background: "#E4E7EC",
                    strokeWidth: "97%",
                    margin: 5,
                },
                dataLabels: {
                    name: {
                        show: true,
                        fontSize: "14px",
                        fontWeight: 600,
                        color: "#98A2B3",
                        offsetY: -10,
                    },
                    value: {
                        show: true,
                        fontSize: "28px",
                        fontWeight: 700,
                        color: "#1D2939",
                        offsetY: 0,
                        formatter: function (val: any) {
                            if (typeof val !== 'number' || isNaN(val)) return "0%";
                            return val.toFixed(2) + "%";
                        },
                    },
                    total: {
                        show: true,
                        label: "Total",
                        fontSize: "14px",
                        fontWeight: 600,
                        color: "#98A2B3",
                        formatter: function () {
                            return "100%";
                        },
                    },
                },
            },
        },
        fill: {
            type: "solid",
            colors: chartColors,
        },
        stroke: {
            lineCap: "round",
        },
        labels: chartLabels,
        tooltip: {
            enabled: true,
            custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                const categoryNames = ['Bien', 'Servicio', 'Obra'];
                const quantities = [categoriaData.bien, categoriaData.servicio, categoriaData.obra];
                const percentage = series[seriesIndex];

                return `<div class="apexcharts-tooltip-custom" style="background: #1F2937; color: white; padding: 8px 12px; border-radius: 6px; font-size: 13px;">
          <div style="font-weight: 600; margin-bottom: 4px;">${categoryNames[seriesIndex]}</div>
          <div>${quantities[seriesIndex].toLocaleString()} licitaciones</div>
          <div>${percentage.toFixed(2)}%</div>
        </div>`;
            },
        },
    };

    const [isOpen, setIsOpen] = useState(false);

    function toggleDropdown() {
        setIsOpen(!isOpen);
    }

    function closeDropdown() {
        setIsOpen(false);
    }

    return (
        <div className="rounded-2xl border border-gray-200 bg-gray-100 dark:border-gray-800 dark:bg-white/[0.03] h-full">
            <div className="px-5 pt-5 bg-white shadow-default rounded-2xl pb-6 dark:bg-gray-900 sm:px-6 sm:pt-6">
                <div className="flex justify-between">
                    <div>
                        <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                            Distribución por Tipo
                        </h3>
                        <p className="mt-1 font-normal text-gray-500 text-theme-sm dark:text-gray-400">
                            Licitaciones por categoría
                        </p>
                    </div>
                    <div className="relative inline-block">
                        <button onClick={toggleDropdown} className="dropdown-toggle">
                            <MoreDotIcon className="text-gray-400 hover:text-gray-700 dark:hover:text-gray-300" />
                        </button>
                        <Dropdown
                            isOpen={isOpen}
                            onClose={closeDropdown}
                            className="w-40 p-2"
                        >
                            <DropdownItem
                                tag="a"
                                onItemClick={closeDropdown}
                                className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
                            >
                                View More
                            </DropdownItem>
                            <DropdownItem
                                tag="a"
                                onItemClick={closeDropdown}
                                className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
                            >
                                Delete
                            </DropdownItem>
                        </Dropdown>
                    </div>
                </div>
                <div className="relative">
                    <div className="max-h-[280px]">
                        {!loading && chartSeries.length > 0 && (
                            <ReactApexChart
                                options={options}
                                series={chartSeries}
                                type="radialBar"
                                height={280}
                            />
                        )}
                        {loading && (
                            <div className="flex items-center justify-center h-[280px]">
                                <p className="text-gray-500 dark:text-gray-400">Cargando...</p>
                            </div>
                        )}
                    </div>
                </div>
                <p className="mx-auto mt-0 w-full max-w-[380px] text-center text-sm text-gray-500 sm:text-base">
                    {categoriaData.total.toLocaleString()} licitaciones distribuidas: BIEN ({porcentajeBien.toFixed(2)}%), SERVICIO ({porcentajeServicio.toFixed(2)}%) y OBRA ({porcentajeObra.toFixed(2)}%).
                </p>
            </div>

            <div className="flex items-center justify-center gap-5 px-6 py-3.5 sm:gap-8 sm:py-5">
                <div>
                    <p className="mb-1 text-center text-theme-xs sm:text-sm" style={{ color: '#465FFF' }}>
                        Bien
                    </p>
                    <p className="flex items-center justify-center gap-1 text-base font-semibold text-gray-800 dark:text-white/90 sm:text-lg">
                        {categoriaData.bien.toLocaleString()}
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M7.60141 2.33683C7.73885 2.18084 7.9401 2.08243 8.16435 2.08243C8.16475 2.08243 8.16516 2.08243 8.16556 2.08243C8.35773 2.08219 8.54998 2.15535 8.69664 2.30191L12.6968 6.29924C12.9898 6.59203 12.9899 7.0669 12.6971 7.3599C12.4044 7.6529 11.9295 7.65306 11.6365 7.36027L8.91435 4.64004L8.91435 13.5C8.91435 13.9142 8.57856 14.25 8.16435 14.25C7.75013 14.25 7.41435 13.9142 7.41435 13.5L7.41435 4.64442L4.69679 7.36025C4.4038 7.65305 3.92893 7.6529 3.63613 7.35992C3.34333 7.06693 3.34348 6.59206 3.63646 6.29926L7.60141 2.33683Z"
                                fill="#039855"
                            />
                        </svg>
                    </p>
                    <p className="text-center text-gray-500 text-theme-xs dark:text-gray-400">
                        {porcentajeBien.toFixed(2)}%
                    </p>
                </div>

                <div className="w-px bg-gray-200 h-7 dark:bg-gray-800"></div>

                <div>
                    <p className="mb-1 text-center text-theme-xs sm:text-sm" style={{ color: '#10B981' }}>
                        Servicio
                    </p>
                    <p className="flex items-center justify-center gap-1 text-base font-semibold text-gray-800 dark:text-white/90 sm:text-lg">
                        {categoriaData.servicio.toLocaleString()}
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M7.60141 2.33683C7.73885 2.18084 7.9401 2.08243 8.16435 2.08243C8.16475 2.08243 8.16516 2.08243 8.16556 2.08243C8.35773 2.08219 8.54998 2.15535 8.69664 2.30191L12.6968 6.29924C12.9898 6.59203 12.9899 7.0669 12.6971 7.3599C12.4044 7.6529 11.9295 7.65306 11.6365 7.36027L8.91435 4.64004L8.91435 13.5C8.91435 13.9142 8.57856 14.25 8.16435 14.25C7.75013 14.25 7.41435 13.9142 7.41435 13.5L7.41435 4.64442L4.69679 7.36025C4.4038 7.65305 3.92893 7.6529 3.63613 7.35992C3.34333 7.06693 3.34348 6.59206 3.63646 6.29926L7.60141 2.33683Z"
                                fill="#039855"
                            />
                        </svg>
                    </p>
                    <p className="text-center text-gray-500 text-theme-xs dark:text-gray-400">
                        {porcentajeServicio.toFixed(2)}%
                    </p>
                </div>

                <div className="w-px bg-gray-200 h-7 dark:bg-gray-800"></div>

                <div>
                    <p className="mb-1 text-center text-theme-xs sm:text-sm" style={{ color: '#F59E0B' }}>
                        Obra
                    </p>
                    <p className="flex items-center justify-center gap-1 text-base font-semibold text-gray-800 dark:text-white/90 sm:text-lg">
                        {categoriaData.obra.toLocaleString()}
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M7.60141 2.33683C7.73885 2.18084 7.9401 2.08243 8.16435 2.08243C8.16475 2.08243 8.16516 2.08243 8.16556 2.08243C8.35773 2.08219 8.54998 2.15535 8.69664 2.30191L12.6968 6.29924C12.9898 6.59203 12.9899 7.0669 12.6971 7.3599C12.4044 7.6529 11.9295 7.65306 11.6365 7.36027L8.91435 4.64004L8.91435 13.5C8.91435 13.9142 8.57856 14.25 8.16435 14.25C7.75013 14.25 7.41435 13.9142 7.41435 13.5L7.41435 4.64442L4.69679 7.36025C4.4038 7.65305 3.92893 7.6529 3.63613 7.35992C3.34333 7.06693 3.34348 6.59206 3.63646 6.29926L7.60141 2.33683Z"
                                fill="#039855"
                            />
                        </svg>
                    </p>
                    <p className="text-center text-gray-500 text-theme-xs dark:text-gray-400">
                        {porcentajeObra.toFixed(2)}%
                    </p>
                </div>
            </div>
        </div>
    );
}
