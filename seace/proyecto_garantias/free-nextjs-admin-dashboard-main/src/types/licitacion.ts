// Interfaces para detalles relacionales
export interface ConsorcioMember {
    nombre_miembro: string;
    ruc_miembro: string;
    porcentaje_participacion: number;
}

export interface AdjudicacionDetalle {
    id_adjudicacion?: string; // Opcional para nuevos registros
    id_contrato?: string;
    ganador_nombre: string;
    ganador_ruc: string;
    monto_adjudicado: number;
    fecha_adjudicacion?: string;
    estado_item?: string;
    entidad_financiera?: string; // Garantía
    tipo_garantia?: string;
    consorcios?: ConsorcioMember[]; // Lista de miembros si es consorcio
}

export interface Licitacion {
    id_convocatoria: number;
    ocid?: string;
    nomenclatura?: string;
    descripcion: string;
    comprador: string;
    categoria: string;
    departamento: string;
    provincia?: string;
    distrito?: string;
    monto_estimado: number;
    moneda?: string;
    fecha_publicacion: string;
    estado_proceso: string;
    tipo_procedimiento?: string;
    fecha_adjudicacion?: string;
    estado_item?: string;  // Estado del item de adjudicación

    // Relación detallada para edición completa
    adjudicaciones?: AdjudicacionDetalle[];

    // Campos calculados de adjudicaciones (mantenidos para compatibilidad de vistas)
    monto_total_adjudicado?: number;
    total_adjudicaciones?: number;
    con_garantia_bancaria?: number;
    entidades_financieras?: string;

    // Nuevos Campos planos (concatenados)
    contratos?: string;
    ganadores?: string;
    ganadores_ruc?: string;
    tipos_garantia?: string;

    // Campos para gestión manual
    origen_tipo?: 'ETL' | 'MANUAL' | 'MODIFICADO';
    usuario_creacion?: string;
    fecha_creacion?: string;
    usuario_modificacion?: string;
    fecha_modificacion?: string;
    estado_registro?: 'ACTIVO' | 'ELIMINADO';
    motivo_eliminacion?: string;
}

export interface SearchFilters {
    search: string;
    departamento: string;
    provincia: string;
    distrito: string;
    estado_proceso: string;
    categoria: string;
    comprador: string;          // Entidad o Consorcio
    aseguradora: string;         // Aseguradora/Entidad Financiera
    year: string;                // Año
    mes: string;                 // Mes
    tipo_garantia?: string;      // Tipo de Garantía
}

// Tipos para módulo de Reportes
export type ReportType = 'entidad' | 'departamento' | 'categoria' | 'estado' | 'personalizado';

export interface ReportConfig {
    tipo: ReportType;
    filtros: SearchFilters;
    agrupacion?: string;
    ordenamiento?: string;
}

export interface ReportResult {
    data: any[];
    totales: {
        garantias: number;
        monto: number;
    };
    metadata: {
        fecha_generacion: string;
        filtros_aplicados: SearchFilters;
    };
}

