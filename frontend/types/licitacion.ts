export interface Licitacion {
    id_convocatoria: string;
    ocid?: string;
    nomenclatura?: string;
    descripcion: string;
    comprador: string;
    categoria?: string;
    tipo_procedimiento?: string;
    monto_estimado?: number;
    moneda?: string;
    fecha_publicacion: string;
    estado_proceso?: string;
    ubicacion_completa?: string;
    departamento?: string;
    provincia?: string;
    distrito?: string;
    monto_total_adjudicado?: number;
    total_adjudicaciones?: number;
    con_garantia_bancaria?: number;
    entidades_financieras?: string;
}

export interface Adjudicacion {
    id_adjudicacion: string;
    ganador_nombre: string;
    ganador_ruc: string;
    monto_adjudicado: number;
    fecha_adjudicacion: string;
    entidad_financiera?: string;
    tipo_garantia?: string;
}

export interface SearchFilters {
    search?: string;
    departamento?: string;
    provincia?: string;
    distrito?: string;
    estado_proceso?: string;
    categoria?: string;
    comprador?: string;
    aseguradora?: string;
    year?: string;
    mes?: string;
    tipo_garantia?: string;
}

export type ReportType = 'entidad' | 'departamento' | 'categoria' | 'estado' | 'personalizado';

export interface ReportData {
    nombre: string;
    garantias: number;
    monto: string; // Formatted string 'S/ 1,234.56'
    departamentos?: number;
    categorias?: string; // Comma separated or count
}
