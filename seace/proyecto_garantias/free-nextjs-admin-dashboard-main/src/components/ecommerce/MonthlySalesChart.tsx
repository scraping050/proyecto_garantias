"use client";
import { ApexOptions } from "apexcharts";
import dynamic from "next/dynamic";
import { MoreDotIcon } from "@/icons";
import { DropdownItem } from "../ui/dropdown/DropdownItem";
import { useState, useEffect } from "react";
import { Dropdown } from "../ui/dropdown/Dropdown";

// Dynamically import the ReactApexChart component
const ReactApexChart = dynamic(() => import("react-apexcharts"), {
    ssr: false,
});

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Interface for estado data
interface EstadoData {
    estado: string;
    total: number;
    retencion: string;
}

// Mapping of full state names to abbreviations (max 5 chars for clean display)
const ESTADO_ABREVIACIONES: Record<string, string> = {
    'CONTRATADO': 'CONTR',
    'DESIERTO': 'DESIE',
    'CONVOCADO': 'CONVO',
    'CONSENTIDO': 'CONSE',
    'RETROTRAIDO_POR_RESOLUCION': 'RETRO',
    'ADJUDICADO': 'ADJUD',
    'CANCELADO': 'CANCE',
    'APELADO': 'APELA',
    'PENDIENTE_DE_REGISTRO_DE_EFECTO': 'PENDI',
    'NO_SUSCRIPCION_CONTRATO_POR_DECISION_ENTIDAD': 'NO_SU',
    'BLOQUEADO': 'BLOQU',
    'CONVOCADO_POR_REINICIO': 'CON_R'
};

export default function MonthlySalesChart() {
    const [estadosData, setEstadosData] = useState<EstadoData[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchEstados = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/reportes/por-estado`);
                const data = await response.json();

                if (data.success && data.data && data.data.estados_proceso) {
                    setEstadosData(data.data.estados_proceso);
                }
            } catch (error) {
                console.error('Error fetching estados:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchEstados();
    }, []);

    // Prepare data for chart - 12 estados + 1 retention bar
    const totalRetenciones = estadosData.reduce((sum, e) => sum + parseInt(String(e.retencion || 0)), 0);

    const categories = [
        ...estadosData.map(e => ESTADO_ABREVIACIONES[e.estado] || e.estado.substring(0, 5)),
        'RETEN' // Additional bar for total retention
    ];

    const seriesData = [
        ...estadosData.map(e => e.total),
        totalRetenciones // Value for retention bar
    ];

    const estadosCompletos = [
        ...estadosData.map(e => e.estado),
        'RETENCIÓN TOTAL'
    ];

    const options: ApexOptions = {
        colors: ["#465fff"],
        chart: {
            fontFamily: "Outfit, sans-serif",
            type: "bar",
            height: 180,
            toolbar: {
                show: false,
            },
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "25%",
                borderRadius: 4,
                borderRadiusApplication: "end",
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
            colors: ["transparent"],
        },
        xaxis: {
            categories: categories,
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
        },
        legend: {
            show: true,
            position: "top",
            horizontalAlign: "left",
            fontFamily: "Outfit",
        },
        yaxis: {
            title: {
                text: undefined,
            },
            logarithmic: true,
            min: 1,
            labels: {
                formatter: function (val: number) {
                    if (val >= 1000) {
                        return (val / 1000).toFixed(0) + 'K';
                    }
                    return Math.round(val).toString();
                },
            },
        },
        grid: {
            yaxis: {
                lines: {
                    show: true,
                },
            },
        },
        fill: {
            opacity: 1,
        },
        tooltip: {
            custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                const estadoCompleto = estadosCompletos[dataPointIndex];
                const valor = series[seriesIndex][dataPointIndex];

                return `
          <div style="
            background: #1f2937;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: Outfit, sans-serif;
            font-size: 13px;
          ">
            <div style="font-weight: 600; margin-bottom: 4px;">${estadoCompleto}</div>
            <div style="color: #9ca3af;">Cantidad: <span style="color: #60a5fa; font-weight: 600;">${valor.toLocaleString()}</span></div>
          </div>
        `;
            },
        },
    };

    const series = [
        {
            name: "Licitaciones",
            data: seriesData,
        },
    ];

    const [isOpen, setIsOpen] = useState(false);

    function toggleDropdown() {
        setIsOpen(!isOpen);
    }

    function closeDropdown() {
        setIsOpen(false);
    }

    return (
        <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white px-5 pt-5 dark:border-gray-800 dark:bg-white/[0.03] sm:px-6 sm:pt-6">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                        Licitaciones por Estado
                    </h3>
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
                            onItemClick={closeDropdown}
                            className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
                        >
                            Ver Más
                        </DropdownItem>
                        <DropdownItem
                            onItemClick={closeDropdown}
                            className="flex w-full font-normal text-left text-gray-500 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
                        >
                            Exportar
                        </DropdownItem>
                    </Dropdown>
                </div>
            </div>

            <div className="-ml-5 pl-2">
                {!loading && estadosData.length > 0 && (
                    <ReactApexChart
                        options={options}
                        series={series}
                        type="bar"
                        height={180}
                    />
                )}
                {loading && (
                    <div className="flex items-center justify-center h-[180px]">
                        <div className="text-gray-500 dark:text-gray-400">Cargando...</div>
                    </div>
                )}
            </div>
        </div>
    );
}
