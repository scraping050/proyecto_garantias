'use client';

interface NotificationFiltersProps {
    typeFilter: string;
    priorityFilter: string;
    onChange: (filters: { type: string; priority: string }) => void;
}

export function NotificationFilters({ typeFilter, priorityFilter, onChange }: NotificationFiltersProps) {
    return (
        <div className="flex gap-2 p-3 bg-gray-50 border-b">
            <select
                value={typeFilter}
                onChange={(e) => onChange({ type: e.target.value, priority: priorityFilter })}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-500 transition-colors"
            >
                <option value="">📌 Todos los tipos</option>
                <option value="licitacion">📋 Licitaciones</option>
                <option value="carta_fianza">💳 Cartas Fianza</option>
                <option value="adjudicacion">🏆 Adjudicaciones</option>
                <option value="consorcio">🤝 Consorcios</option>
                <option value="reporte">📊 Reportes</option>
                <option value="sistema">⚙️ Sistema</option>
            </select>

            <select
                value={priorityFilter}
                onChange={(e) => onChange({ type: typeFilter, priority: e.target.value })}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-500 transition-colors"
            >
                <option value="">⭐ Todas las prioridades</option>
                <option value="high">🔴 Alta</option>
                <option value="medium">🟡 Media</option>
                <option value="low">🔵 Baja</option>
            </select>

            {(typeFilter || priorityFilter) && (
                <button
                    onClick={() => onChange({ type: '', priority: '' })}
                    className="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm hover:bg-gray-300 transition-colors"
                    title="Limpiar filtros"
                >
                    <i className="fas fa-times"></i>
                </button>
            )}
        </div>
    );
}
