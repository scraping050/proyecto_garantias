export interface Notification {
    id: number;
    id_convocatoria: string;
    tipo: string;
    titulo: string;
    mensaje: string;
    estado_anterior: string | null;
    estado_nuevo: string | null;
    leida: boolean;
    fecha_creacion: string;
    fecha_lectura: string | null;
    metadata: {
        comprador?: string;
        monto_estimado?: number;
        departamento?: string;
        categoria?: string;
    } | null;
    // Campos adicionales del JOIN
    licitacion_descripcion?: string;
    comprador?: string;
    monto_estimado?: number;
    departamento?: string;
    categoria?: string;
    ocid?: string;
}

export interface NotificationsResponse {
    success: boolean;
    data: Notification[];
    pagination: {
        page: number;
        per_page: number;
        total: number;
        total_pages: number;
    };
}

export interface NotificationCountResponse {
    success: boolean;
    count: number;
}
