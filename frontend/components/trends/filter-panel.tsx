'use client'

import { FilterOptions, TendenciasFilters } from '@/hooks/use-tendencias'
import { X, Filter, Search } from 'lucide-react'

interface FilterPanelProps {
    filters: TendenciasFilters
    filterOptions?: FilterOptions
    onFilterChange: (filters: Partial<TendenciasFilters>) => void
    onReset: () => void

}

export function FilterPanel({
    filters,
    filterOptions,
    onFilterChange,
    onReset,

}: FilterPanelProps) {
    const activeFiltersCount = Object.values(filters).filter(v => v !== undefined && v !== '').length

    return (
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 mb-8">
            <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center">
                        <Filter className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Filtros</h3>
                    {activeFiltersCount > 0 && (
                        <span className="px-3 py-1.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-xs font-bold rounded-full shadow-sm">
                            {activeFiltersCount} activos
                        </span>
                    )}
                </div>
                {activeFiltersCount > 0 && (
                    <button
                        onClick={onReset}
                        className="group flex items-center gap-2 px-4 py-2.5 text-sm font-bold text-gray-700 dark:text-gray-300 hover:text-white hover:bg-gradient-to-r hover:from-gray-600 hover:to-gray-700 bg-gray-100 dark:bg-gray-700 rounded-xl transition-all duration-300 hover:shadow-md hover:-translate-y-0.5"
                    >
                        <X className="w-4 h-4 group-hover:rotate-90 transition-transform duration-300" />
                        Limpiar Filtros
                    </button>
                )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                {/* Objeto Contratación */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Objeto de Contratación
                    </label>
                    <select
                        value={filters.objeto_contratacion || ''}
                        onChange={(e) => onFilterChange({ objeto_contratacion: e.target.value || undefined })}
                        className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-500 cursor-pointer bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-medium text-sm"
                    >
                        <option value="">Todos</option>
                        {filterOptions?.objetos_contratacion.map((obj) => (
                            <option key={obj} value={obj}>{obj}</option>
                        ))}
                    </select>
                </div>

                {/* Tipo Procedimiento */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Tipo de Procedimiento
                    </label>
                    <select
                        value={filters.tipo_procedimiento || ''}
                        onChange={(e) => onFilterChange({ tipo_procedimiento: e.target.value || undefined })}
                        className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-500 cursor-pointer bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-medium text-sm"
                    >
                        <option value="">Todos</option>
                        {filterOptions?.tipos_procedimiento.map((tipo) => (
                            <option key={tipo} value={tipo}>{tipo}</option>
                        ))}
                    </select>
                </div>

                {/* Estado Proceso */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Estado del Proceso
                    </label>
                    <select
                        value={filters.estado_proceso || ''}
                        onChange={(e) => onFilterChange({ estado_proceso: e.target.value || undefined })}
                        className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-500 cursor-pointer bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-medium text-sm"
                    >
                        <option value="">Todos</option>
                        {filterOptions?.estados_proceso.map((estado) => (
                            <option key={estado} value={estado}>{estado}</option>
                        ))}
                    </select>
                </div>

                {/* Departamento */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Departamento
                    </label>
                    <select
                        value={filters.departamento || ''}
                        onChange={(e) => onFilterChange({ departamento: e.target.value || undefined })}
                        className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-500 cursor-pointer bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-medium text-sm"
                    >
                        <option value="">Todos</option>
                        {filterOptions?.departamentos.map((dept) => (
                            <option key={dept} value={dept}>{dept}</option>
                        ))}
                    </select>
                </div>

                {/* Banco Garantía */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Banco de Garantía
                    </label>
                    <select
                        value={filters.banco_garantia || ''}
                        onChange={(e) => onFilterChange({ banco_garantia: e.target.value || undefined })}
                        className="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-500 cursor-pointer bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-medium text-sm"
                    >
                        <option value="">Todos</option>
                        {filterOptions?.bancos_garantia.map((banco) => (
                            <option key={banco} value={banco}>{banco}</option>
                        ))}
                    </select>
                </div>
            </div>


        </div>
    )
}
