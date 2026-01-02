"use client";
import React from "react";
import { VectorMap } from "@react-jvectormap/core";
import { worldMill } from "@react-jvectormap/world";

export interface MapOneProps {
    data: { [key: string]: number }; // e.g., { "PE-LIM": 100, "PE-ARE": 50 }
}

export default function MapOne({ data }: MapOneProps) {
    return (
        <div className="col-span-12 rounded-[10px] bg-white px-7.5 py-6 shadow-1 dark:bg-gray-dark dark:shadow-card xl:col-span-7">
            <h4 className="mb-2 text-body-2xlg font-bold text-dark dark:text-white">
                Distribución Geográfica
            </h4>
            <div className="h-[420px]">
                <VectorMap
                    map={worldMill}
                    backgroundColor="transparent"
                    zoomOnScroll={false}
                    containerStyle={{
                        width: "100%",
                        height: "100%",
                    }}
                    regionStyle={{
                        initial: {
                            fill: "#E8E8E8",
                            fillOpacity: 1,
                            stroke: "none",
                            strokeWidth: 0,
                            strokeOpacity: 1,
                        },
                        hover: {
                            fillOpacity: 0.8,
                            cursor: "pointer",
                        },
                        selected: {
                            fill: "#465FFF",
                        },
                    }}
                    series={{
                        regions: [
                            {
                                scale: ["#9CB9FF", "#465FFF"], // Color gradient
                                values: data, // Data mapping
                                // @ts-ignore
                                min: 0,
                                // @ts-ignore
                                max: 100,
                                // @ts-ignore
                                attribute: "fill",
                            },
                        ],
                    }}
                    // Customize tooltip
                    // Customize tooltip
                    // @ts-ignore
                    onRegionTipShow={function (e, label, code) {
                        // @ts-ignore
                        label.html(`
                  <div class="bg-white text-dark px-2 py-1 rounded shadow-lg text-sm">
                    <p class="font-bold">${label.html()}</p>
                    <p>Licitaciones: ${data[code] || 0}</p>
                  </div>
                `);
                    }}
                />
            </div>
        </div>
    );
}
