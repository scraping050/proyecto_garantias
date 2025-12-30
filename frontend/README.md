# SEACE Monitor - Frontend

Sistema de Inteligencia de Negocios para monitoreo de garantías bancarias en licitaciones públicas del SEACE. Frontend construido con Next.js 14, TypeScript, Tailwind CSS y Shadcn UI.

## 🚀 Características

- **Next.js 14** con App Router y Server Components
- **TypeScript** con tipado estricto
- **Tailwind CSS** para estilos utility-first
- **Shadcn UI** componentes accesibles y personalizables
- **TanStack Query** para data fetching y caching
- **Recharts** para visualizaciones de datos
- **Dark Mode** con next-themes
- **Responsive Design** mobile-first

## 📦 Instalación

### Prerrequisitos

- Node.js 18+ y npm
- Backend FastAPI corriendo en `http://localhost:8000`

### Pasos de Instalación

1. **Navegar al directorio del frontend:**

```bash
cd c:\laragon\www\proyecto_garantias\frontend
```

2. **Instalar dependencias:**

```bash
npm install
```

3. **Instalar componentes de Shadcn UI:**

El proyecto ya incluye los componentes necesarios, pero si necesitas agregar más:

```bash
npx shadcn-ui@latest add [component-name]
```

Componentes ya instalados:
- button
- badge
- card
- input
- (otros componentes están incluidos en el código)

4. **Ejecutar en modo desarrollo:**

```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:3000**

## 🏗️ Estructura del Proyecto

```
frontend/
├── app/
│   ├── layout.tsx              # Layout raíz con Sidebar y TopBar
│   ├── page.tsx                # Página principal (redirige a dashboard)
│   ├── globals.css             # Estilos globales y variables CSS
│   ├── dashboard/
│   │   └── page.tsx            # Dashboard con KPIs y gráficos
│   └── licitaciones/
│       ├── page.tsx            # Explorador de licitaciones
│       └── [id]/
│           └── page.tsx        # Vista de detalle
├── components/
│   ├── ui/                     # Componentes base de Shadcn UI
│   │   ├── button.tsx
│   │   ├── badge.tsx
│   │   ├── card.tsx
│   │   └── input.tsx
│   ├── layout/
│   │   ├── sidebar.tsx         # Navegación lateral colapsable
│   │   └── top-bar.tsx         # Barra superior con breadcrumbs
│   ├── data/
│   │   ├── bank-badge.tsx      # Badge inteligente para bancos
│   │   └── status-badge.tsx    # Badge para estados
│   └── providers.tsx           # TanStack Query y Theme providers
├── lib/
│   ├── api.ts                  # Cliente API para FastAPI
│   ├── utils.ts                # Utilidades (cn, colores, etc.)
│   └── formatters.ts           # Formateadores (moneda, fecha, etc.)
├── types/
│   └── index.ts                # Interfaces TypeScript
├── hooks/
│   └── use-licitaciones.ts     # Hooks de TanStack Query
├── tailwind.config.ts          # Configuración de Tailwind
├── tsconfig.json               # Configuración de TypeScript
├── next.config.js              # Configuración de Next.js
└── package.json                # Dependencias
```

## 🎨 Componentes Clave

### BankBadge

Componente inteligente que muestra badges de bancos con colores específicos:

```tsx
import { BankBadge } from '@/components/data/bank-badge'

<BankBadge bank="SCOTIABANK" /> // Rojo
<BankBadge bank="BCP" />        // Azul oscuro
<BankBadge bank="FOGAPI" />     // Ámbar (garantía líquida)
<BankBadge bank={null} />       // Gris "Sin Garantía"
```

### Formatters

Utilidades para formatear datos:

```tsx
import { formatCurrency, formatDate, formatRUC } from '@/lib/formatters'

formatCurrency(1250000)     // "S/ 1,250,000.00"
formatDate("2024-01-15")    // "15/01/2024"
formatRUC("20123456789")    // "20-12345678-9"
```

## 🔌 Integración con Backend

El frontend se conecta al backend FastAPI en `http://localhost:8000`. Los endpoints utilizados son:

- `GET /api/dashboard/kpis` - KPIs del dashboard
- `GET /api/licitaciones` - Lista paginada de licitaciones
- `GET /api/licitaciones/{id}` - Detalle de licitación

### Configuración de API

Edita `lib/api.ts` si necesitas cambiar la URL del backend:

```typescript
const API_BASE_URL = 'http://localhost:8000' // Cambiar aquí
```

## 📊 Páginas

### Dashboard (`/dashboard`)

- KPIs: Total adjudicado, total licitaciones, ratio de garantías
- Gráfico de barras: Top 5 bancos emisores
- Gráfico de barras: Top 5 entidades públicas

### Licitaciones (`/licitaciones`)

- Búsqueda global con debounce
- Filtros por RUC, banco, fechas
- Paginación del lado del servidor
- Sincronización con URL (enlaces compartibles)
- Tabla responsive con acciones

### Detalle (`/licitaciones/[id]`)

- Layout 2/3 + 1/3
- Información completa del proceso
- Datos del ganador
- Análisis de consorcio con gráfico de pastel
- Botones para copiar información

## 🎨 Temas y Estilos

### Dark Mode

El tema se puede cambiar usando el botón en la TopBar. El estado se persiste en localStorage.

### Colores de Bancos

Definidos en `tailwind.config.ts`:

- **Scotiabank**: `#ED1C24` (Rojo)
- **BCP**: `#002A8D` (Azul oscuro)
- **BBVA**: `#004481` (Azul)
- **Interbank**: `#00A0DF` (Azul claro)
- **FOGAPI/SECREX**: `#F59E0B` (Ámbar)

## 🔧 Scripts Disponibles

```bash
npm run dev      # Desarrollo con hot-reload
npm run build    # Build de producción
npm run start    # Servidor de producción
npm run lint     # Linter ESLint
```

## 📝 Notas Técnicas

### URL State Management

Los filtros y la paginación se sincronizan con la URL usando `useSearchParams`:

```
/licitaciones?page=2&limit=20&search=municipalidad
```

Esto permite:
- Enlaces compartibles
- Navegación con botones atrás/adelante
- Estado persistente en recargas

### Data Fetching

TanStack Query maneja:
- Caching automático (5 min para KPIs, 2 min para listas)
- Refetch en background
- Estados de loading y error
- Invalidación de cache

### Performance

- Server Components por defecto
- Client Components solo donde hay interactividad
- Lazy loading de imágenes
- Debounce en búsquedas (500ms)
- Paginación del lado del servidor

## 🐛 Troubleshooting

### Error de conexión al backend

Verifica que:
1. El backend FastAPI esté corriendo en `http://localhost:8000`
2. CORS esté habilitado en el backend
3. No haya firewall bloqueando el puerto 8000

### Componentes de Shadcn UI no se ven

Asegúrate de que:
1. `tailwind.config.ts` incluya las rutas correctas
2. `globals.css` tenga las variables CSS
3. `npm install` se haya ejecutado correctamente

### Errores de TypeScript

Ejecuta:
```bash
npm run build
```

Para ver todos los errores de tipo.

## 📚 Recursos

- [Next.js Documentation](https://nextjs.org/docs)
- [Shadcn UI](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Tailwind CSS](https://tailwindcss.com/)
- [Recharts](https://recharts.org/)

---

**Versión:** 1.0.0  
**Framework:** Next.js 14  
**UI Library:** Shadcn UI  
**Data Fetching:** TanStack Query
