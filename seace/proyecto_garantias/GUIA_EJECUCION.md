# 🚀 Guía para Ejecutar el Dashboard SEACE

## Opción 1: Ver Demo Standalone (SIN NECESIDAD DE NPM)

### ✅ Forma más rápida - Solo abrir en navegador

1. Navega a la carpeta:
   ```
   c:\laragon\www\proyecto_garantias\frontend\
   ```

2. Abre el archivo `demo.html` con tu navegador favorito:
   - Doble click en `demo.html`
   - O click derecho → Abrir con → Chrome/Firefox/Edge

3. ¡Listo! Verás el Dashboard con:
   - ✅ Header con navegación
   - ✅ 4 KPIs
   - ✅ Filtros de búsqueda
   - ✅ Tabla de licitaciones
   - ✅ Diseño responsive

**Nota:** Este demo es estático (no conecta con el backend), pero muestra el diseño completo.

---

## Opción 2: Ejecutar Aplicación Completa (CON BACKEND)

### Requisitos Previos
- Node.js instalado
- npm disponible en PATH

### Paso 1: Abrir Terminal de Laragon

1. Abre Laragon
2. Click en "Terminal" o "CMDER"
3. Esto abrirá una terminal con Node.js configurado

### Paso 2: Instalar Dependencias del Frontend

```bash
cd c:\laragon\www\proyecto_garantias\frontend
npm install
```

Esto instalará:
- React y React DOM
- React Router
- Axios
- Chart.js
- Y todas las demás dependencias

### Paso 3: Iniciar Backend (Terminal 1)

```bash
cd c:\laragon\www\proyecto_garantias\backend
npm run dev
```

Deberías ver:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚀 API Garantías SEACE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ Servidor corriendo en: http://localhost:5000
```

### Paso 4: Iniciar Frontend (Terminal 2 - Nueva terminal)

```bash
cd c:\laragon\www\proyecto_garantias\frontend
npm run dev
```

Deberías ver:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Paso 5: Abrir en Navegador

Visita: `http://localhost:5173`

---

## 🎯 ¿Qué verás?

### Dashboard Completo con:

**Header:**
- Logo 🏛️ "Dashboard SEACE"
- 5 botones de navegación

**KPIs (4 tarjetas):**
- 📊 Total Licitaciones: 10,043
- 💰 Monto Total: S/ 45.6B
- 🏦 Garantías Bancarias: 2,850 (37.43%)
- 📝 Retención: 4,764 (62.57%)

**Filtros:**
- Búsqueda por texto
- Filtro por departamento
- Filtro por categoría
- Botón limpiar

**Tabla:**
- 8 columnas de información
- 20 licitaciones por página
- Paginación funcional
- Datos en tiempo real del backend

---

## 📱 Prueba Responsive

Abre las DevTools del navegador (F12) y prueba estos tamaños:

- **Desktop (1920x1080):** Grid 4 columnas para KPIs
- **Tablet (768x1024):** Grid 2 columnas para KPIs
- **Mobile (375x667):** 1 columna, navegación compacta

---

## ❌ Solución de Problemas

### Error: "npm no se reconoce"
**Solución:** Usa la terminal de Laragon o agrega Node.js al PATH del sistema

### Error: "Cannot GET /"
**Solución:** Asegúrate de que el frontend esté corriendo en puerto 5173

### Error: "Network Error" en el dashboard
**Solución:** Verifica que el backend esté corriendo en puerto 5000

### La tabla está vacía
**Solución:** 
1. Verifica que MySQL esté corriendo en Laragon
2. Verifica que la base de datos `garantias_seace` exista
3. Verifica que haya datos en la tabla `licitaciones_cabecera`

---

## 🎨 Características del Diseño

✅ Paleta azul profesional
✅ Tipografía Inter de Google Fonts
✅ Sombras sutiles y transiciones suaves
✅ Iconos emoji para mejor UX
✅ Badges de colores por categoría
✅ Hover effects en tarjetas y filas
✅ 100% responsive

---

## 📂 Estructura de Archivos

```
frontend/
├── demo.html              ← DEMO STANDALONE (abre este)
├── package.json           ← Dependencias
├── vite.config.js         ← Configuración Vite
├── index.html             ← HTML principal
└── src/
    ├── main.jsx           ← Entry point
    ├── App.jsx            ← App principal
    ├── router.jsx         ← Rutas
    ├── api/               ← Servicios API
    ├── components/        ← Componentes React
    ├── pages/             ← Páginas
    ├── styles/            ← Estilos globales
    └── utils/             ← Utilidades
```

---

## 🚀 Próximos Pasos

Una vez que veas el Dashboard funcionando, podemos continuar con:

1. **Módulo 2: Estadísticas** - Gráficos interactivos
2. **Módulo 3: Gestión Manual** - CRUD de licitaciones
3. **Módulo 4: Notificaciones** - Sistema de alertas
4. **Módulo 5: Reportes** - Generación PDF/Word

---

## 💡 Recomendación

**Para ver el diseño rápidamente:** Abre `demo.html` en tu navegador

**Para ver la aplicación completa:** Sigue los pasos de la Opción 2
