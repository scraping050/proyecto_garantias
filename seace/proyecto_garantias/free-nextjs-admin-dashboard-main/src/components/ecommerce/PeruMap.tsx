"use client";
import React, { useState, useMemo } from "react";
import { ComposableMap, Geographies, Geography, ZoomableGroup } from "react-simple-maps";
import { Plus, Minus, Maximize2 } from "lucide-react";
import { scaleLinear } from "d3-scale";

// GeoJSON path in public folder
const GEO_URL = "/data/geo/peru_departments.geojson";

interface DepartmentData {
    departamento: string;
    total: number;
    monto_total: string;
}

interface PeruMapProps {
    departments: DepartmentData[];
    onSelect?: (department: string | null) => void;
}

const PeruMap: React.FC<PeruMapProps> = ({ departments, onSelect }) => {
    // Estado para el tooltip: nombre, total, y posición (x, y)
    const [tooltipData, setTooltipData] = useState<{ name: string; total: number; x: number; y: number } | null>(null);
    const [selectedDept, setSelectedDept] = useState<string | null>(null);

    // Estado para el zoom y centro
    const [position, setPosition] = useState({ coordinates: [-74.5, -9.5] as [number, number], zoom: 1 });

    // Normalizar nombres y calcular máximo para escala de color
    const { normalizedData, maxTotal } = useMemo(() => {
        const map = new Map();
        let max = 0;
        departments.forEach((d) => {
            map.set(d.departamento.toUpperCase(), d);
            if (d.total > max) max = d.total;
        });
        return { normalizedData: map, maxTotal: max };
    }, [departments]);

    // Escala de color "Heatmap Holográfico"
    const colorScale = scaleLinear<string>()
        .domain([0, maxTotal || 100])
        .range(["#1e293b", "#06b6d4"]); // Slate-800 to Cyan-500

    // Manejadores de Zoom
    const handleZoomIn = (e: React.MouseEvent) => {
        e.stopPropagation();
        setPosition((pos) => ({ ...pos, zoom: Math.min(4, pos.zoom * 1.5) }));
    };

    const handleZoomOut = (e: React.MouseEvent) => {
        e.stopPropagation();
        setPosition((pos) => ({ ...pos, zoom: Math.max(1, pos.zoom / 1.5) }));
    };

    const handleReset = (e: React.MouseEvent) => {
        e.stopPropagation();
        setPosition({ coordinates: [-74.5, -9.5], zoom: 1 });
        setSelectedDept(null);
        if (onSelect) onSelect(null);
    };

    const handleMoveEnd = (position: { coordinates: [number, number], zoom: number }) => {
        setPosition(position);
    };

    const handleDepartmentClick = (deptName: string) => {
        const newSelection = selectedDept === deptName ? null : deptName;
        setSelectedDept(newSelection);
        if (onSelect) onSelect(newSelection);
    };

    return (
        <div className="relative w-full h-[500px] flex items-center justify-center overflow-hidden rounded-2xl bg-white border border-slate-200 shadow-sm group selection-none">

            {/* Grid Decorativo de Fondo */}
            <div className="absolute inset-0 opacity-10 pointer-events-none"
                style={{
                    backgroundImage: "radial-gradient(circle at 2px 2px, #94a3b8 1px, transparent 0)",
                    backgroundSize: "24px 24px"
                }}>
            </div>

            {/* Controles HUD */}
            <div className="absolute top-6 right-6 flex flex-col gap-3 z-50">
                <div className="flex flex-col bg-white/80 backdrop-blur-md border border-slate-200 rounded-xl p-1.5 shadow-lg ring-1 ring-slate-100">
                    <button
                        type="button"
                        onClick={handleZoomIn}
                        className="p-2.5 text-slate-600 hover:text-cyan-600 hover:bg-cyan-50 rounded-lg transition-all active:scale-95"
                        title="Acercar"
                    >
                        <Plus size={18} strokeWidth={2.5} />
                    </button>
                    <div className="h-[1px] w-full bg-slate-200 my-1"></div>
                    <button
                        type="button"
                        onClick={handleZoomOut}
                        className="p-2.5 text-slate-600 hover:text-cyan-600 hover:bg-cyan-50 rounded-lg transition-all active:scale-95"
                        title="Alejar"
                    >
                        <Minus size={18} strokeWidth={2.5} />
                    </button>
                    <div className="h-[1px] w-full bg-slate-200 my-1"></div>
                    <button
                        type="button"
                        onClick={handleReset}
                        className="p-2.5 text-slate-600 hover:text-cyan-600 hover:bg-cyan-50 rounded-lg transition-all active:scale-95"
                        title="Restablecer vista"
                    >
                        <Maximize2 size={18} strokeWidth={2.5} />
                    </button>
                </div>
            </div>

            <ComposableMap
                projection="geoMercator"
                projectionConfig={{
                    scale: 1800,
                    center: [-74.5, -9.5]
                }}
                className="w-full h-full z-10"
                style={{ width: "100%", height: "100%" }}
            >
                <defs>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                    <filter id="shadow-map" x="-50%" y="-50%" width="200%" height="200%">
                        <feDropShadow dx="0" dy="4" stdDeviation="6" floodColor="#000" floodOpacity="0.15" />
                    </filter>
                    <filter id="selected-glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="5" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                <ZoomableGroup
                    zoom={position.zoom}
                    center={position.coordinates}
                    onMoveEnd={handleMoveEnd}
                    minZoom={1}
                    maxZoom={6}
                >
                    <Geographies geography={GEO_URL}>
                        {({ geographies }) =>
                            geographies.map((geo) => {
                                const deptName = geo.properties.NOMBDEP || "";
                                const data = normalizedData.get(deptName);
                                const total = data?.total || 0;
                                const isSelected = selectedDept === deptName;

                                const baseColor = total > 0 ? colorScale(total) : "#1e293b";

                                return (
                                    <Geography
                                        key={geo.rsmKey}
                                        geography={geo}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleDepartmentClick(deptName);
                                        }}
                                        onMouseEnter={(e) => {
                                            const { clientX, clientY } = e;
                                            setTooltipData({
                                                name: deptName,
                                                total: total,
                                                x: clientX,
                                                y: clientY
                                            });
                                        }}
                                        onMouseMove={(e) => {
                                            setTooltipData(prev => prev ? { ...prev, x: e.clientX, y: e.clientY } : null);
                                        }}
                                        onMouseLeave={() => {
                                            setTooltipData(null);
                                        }}
                                        style={{
                                            default: {
                                                fill: isSelected ? "#06b6d4" : baseColor,
                                                stroke: isSelected ? "#fff" : "rgba(255, 255, 255, 0.4)",
                                                strokeWidth: isSelected ? 2 : 0.8,
                                                outline: "none",
                                                transition: "all 0.3s ease",
                                                filter: isSelected ? "url(#selected-glow)" : "url(#shadow-map)",
                                                zIndex: isSelected ? 100 : 1
                                            },
                                            hover: {
                                                fill: "#22d3ee",
                                                stroke: "#fff",
                                                strokeWidth: 2,
                                                outline: "none",
                                                cursor: "pointer",
                                                filter: "url(#glow) drop-shadow(0 0 10px rgba(34, 211, 238, 0.5))",
                                                zIndex: 100,
                                            },
                                            pressed: {
                                                fill: "#0891b2",
                                                stroke: "#fff",
                                                strokeWidth: 2,
                                                outline: "none",
                                            },
                                        }}
                                    />
                                );
                            })
                        }
                    </Geographies>
                </ZoomableGroup>
            </ComposableMap>

            {/* HUD Info Panel */}
            <div className="absolute bottom-6 left-6 z-40">
                <div className="bg-white/80 backdrop-blur-md border border-slate-200 rounded-xl px-4 py-3 shadow-lg">
                    <div className="text-[10px] items-center gap-2 text-slate-500 font-bold tracking-widest uppercase mb-1 flex">
                        <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></div>
                        Actividad
                    </div>
                    <div className="h-1.5 w-32 bg-gradient-to-r from-slate-400 to-cyan-500 rounded-full mt-1"></div>
                    <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-mono">
                        <span>Baja</span>
                        <span>Alta</span>
                    </div>
                </div>
            </div>

            {/* Tooltip HUD Compacto */}
            {tooltipData && (
                <div
                    className="fixed z-[100] pointer-events-none"
                    style={{ left: tooltipData.x, top: tooltipData.y }}
                >
                    <div className="transform -translate-x-1/2 -translate-y-full mt-[-10px] bg-slate-900/95 backdrop-blur-xl px-3 py-2.5 rounded-lg border border-slate-700 shadow-xl min-w-[140px]">
                        {/* Línea decorativa conectora reducida */}
                        <div className="absolute bottom-[-5px] left-1/2 -translate-x-1/2 w-2.5 h-2.5 bg-slate-900 border-r border-b border-slate-700 rotate-45"></div>

                        <div className="flex flex-col gap-0.5">
                            <span className="text-[9px] font-bold text-cyan-400 tracking-[0.15em] uppercase">Región</span>
                            <h3 className="text-base font-bold text-white font-heading leading-tight">{tooltipData.name}</h3>

                            <div className="mt-1.5 pt-1.5 border-t border-white/10 flex items-center justify-between gap-3">
                                <span className="text-[10px] text-slate-400 font-medium">Licitaciones</span>
                                <span className="text-base font-bold text-white font-mono tracking-tight leading-none">
                                    {tooltipData.total.toLocaleString()}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PeruMap;
