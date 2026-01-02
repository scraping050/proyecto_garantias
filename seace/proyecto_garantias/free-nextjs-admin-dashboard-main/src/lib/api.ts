// API client para conectar con el backend de licitaciones
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export interface DepartmentData {
  departamento: string;
  total: number;
  monto_total: number;
  garantias_bancarias: number;
  garantias_retencion: number;
  porcentaje: string;
}

export interface MapDataResponse {
  success: boolean;
  data: DepartmentData[];
  total_licitaciones: number;
  departamentos_con_datos: number;
}

/**
 * Obtiene los datos del mapa de Perú desde el backend
 */
export async function getMapData(filters?: Record<string, any>): Promise<MapDataResponse> {
  try {
    const params = new URLSearchParams();

    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, String(value));
        }
      });
    }

    const url = `${API_BASE_URL}/api/charts/departamentos-mapa${params.toString() ? `?${params.toString()}` : ''}`;

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store', // Siempre obtener datos frescos
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching map data:', error);
    throw error;
  }
}

/**
 * Obtiene los KPIs principales
 */
export async function getKPIs() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/charts/kpis`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching KPIs:', error);
    throw error;
  }
}
