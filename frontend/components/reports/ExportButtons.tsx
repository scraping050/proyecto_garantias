import React, { useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import { Fragment } from "react";

interface Props {
    onExport: (format: "pdf" | "excel" | "csv") => void;
    loading?: boolean;
    disabled?: boolean;
}

export const ExportButtons: React.FC<Props> = ({ onExport, loading, disabled }) => {
    return (
        <div className="relative inline-block text-left">
            <Menu as="div" className="relative inline-block text-left">
                <div>
                    <Menu.Button
                        disabled={disabled || loading}
                        className="inline-flex w-full justify-center rounded-lg border border-slate-200/60 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700/60 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                    >
                        {loading ? "Exportando..." : "Exportar"}
                        <svg
                            className="-mr-1 ml-2 h-5 w-5"
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                            aria-hidden="true"
                        >
                            <path
                                fillRule="evenodd"
                                d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                                clipRule="evenodd"
                            />
                        </svg>
                    </Menu.Button>
                </div>

                <Transition
                    as={Fragment}
                    enter="transition ease-out duration-100"
                    enterFrom="transform opacity-0 scale-95"
                    enterTo="transform opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leaveFrom="transform opacity-100 scale-100"
                    leaveTo="transform opacity-0 scale-95"
                >
                    <Menu.Items className="absolute right-0 mt-2 w-40 origin-top-right divide-y divide-gray-100 rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-slate-800 dark:divide-slate-700 dark:ring-slate-700">
                        <div className="p-1">
                            <Menu.Item>
                                {({ active }) => (
                                    <button
                                        onClick={() => onExport("pdf")}
                                        className={`${active ? "bg-indigo-50 text-indigo-700 dark:bg-slate-700 dark:text-white" : "text-gray-900 dark:text-gray-200"
                                            } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                    >
                                        <svg className="mr-2 h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                        </svg>
                                        PDF
                                    </button>
                                )}
                            </Menu.Item>
                            <Menu.Item>
                                {({ active }) => (
                                    <button
                                        onClick={() => onExport("excel")}
                                        className={`${active ? "bg-indigo-50 text-indigo-700 dark:bg-slate-700 dark:text-white" : "text-gray-900 dark:text-gray-200"
                                            } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                    >
                                        <svg className="mr-2 h-4 w-4 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        Excel
                                    </button>
                                )}
                            </Menu.Item>
                            <Menu.Item>
                                {({ active }) => (
                                    <button
                                        onClick={() => onExport("csv")}
                                        className={`${active ? "bg-indigo-50 text-indigo-700 dark:bg-slate-700 dark:text-white" : "text-gray-900 dark:text-gray-200"
                                            } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                    >
                                        <svg className="mr-2 h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        CSV
                                    </button>
                                )}
                            </Menu.Item>
                        </div>
                    </Menu.Items>
                </Transition>
            </Menu>
        </div>
    );
};
