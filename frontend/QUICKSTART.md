# 🚀 Guía Rápida de Inicio - SEACE Monitor Frontend

## ✅ Estado del Proyecto

**Todos los archivos han sido creados exitosamente:**

- ✅ 25+ archivos de código fuente
- ✅ Configuración completa (TypeScript, Tailwind, Next.js)
- ✅ Componentes UI (Button, Badge, Card, Input)
- ✅ Componentes personalizados (BankBadge, StatusBadge, Sidebar, TopBar)
- ✅ 3 páginas principales (Dashboard, Licitaciones, Detalle)
- ✅ Hooks de TanStack Query
- ✅ Utilidades y formateadores
- ✅ Scripts de instalación

---

## 📋 Pasos para Ejecutar

### Opción 1: Usando Scripts Automáticos (Recomendado)

1. **Abrir Explorador de Windows:**
   - Navegar a: `C:\laragon\www\proyecto_garantias\frontend`

2. **Doble clic en `install.bat`:**
   - Esto instalará todas las dependencias automáticamente
   - Esperar a que termine (puede tomar 2-3 minutos)

3. **Doble clic en `start.bat`:**
   - Esto iniciará el servidor de desarrollo
   - Se abrirá en: `http://localhost:3000`

### Opción 2: Usando Comandos Manuales

```bash
# 1. Abrir PowerShell o CMD
cd C:\laragon\www\proyecto_garantias\frontend

# 2. Instalar dependencias
npm install

# 3. Instalar paquetes adicionales
npm install tailwindcss-animate next-themes

# 4. Iniciar servidor de desarrollo
npm run dev
```

---

## 🌐 Acceder al Frontend

Una vez que el servidor esté corriendo:

1. **Abrir navegador**
2. **Ir a:** `http://localhost:3000`
3. **Deberías ver:**
   - Sidebar con navegación
   - Dashboard con KPIs
   - Gráficos de Recharts
   - Tema claro/oscuro funcional

---

## 🔧 Verificación Previa

### Antes de instalar, verifica:

1. **Node.js instalado:**
   ```bash
   node --version
   # Debe mostrar v18.x o superior
   ```

2. **npm instalado:**
   ```bash
   npm --version
   # Debe mostrar 9.x o superior
   ```

3. **Backend corriendo:**
   - El backend FastAPI debe estar en: `http://localhost:8000`
   - Verifica abriendo: `http://localhost:8000/docs`

---

## 📁 Estructura Creada

```
frontend/
├── app/
│   ├── layout.tsx              ✅ Layout principal
│   ├── page.tsx                ✅ Página de inicio
│   ├── globals.css             ✅ Estilos globales
│   ├── dashboard/
│   │   └── page.tsx            ✅ Dashboard con KPIs
│   └── licitaciones/
│       ├── page.tsx            ✅ Explorador
│       └── [id]/
│           └── page.tsx        ✅ Vista detalle
├── components/
│   ├── ui/                     ✅ Componentes Shadcn UI
│   ├── layout/                 ✅ Sidebar y TopBar
│   ├── data/                   ✅ BankBadge y StatusBadge
│   └── providers.tsx           ✅ TanStack Query provider
├── lib/
│   ├── api.ts                  ✅ Cliente API
│   ├── utils.ts                ✅ Utilidades
│   └── formatters.ts           ✅ Formateadores
├── types/
│   └── index.ts                ✅ Interfaces TypeScript
├── hooks/
│   └── use-licitaciones.ts     ✅ Hooks de datos
├── install.bat                 ✅ Script de instalación
├── start.bat                   ✅ Script de inicio
├── package.json                ✅ Dependencias
├── tsconfig.json               ✅ Config TypeScript
├── tailwind.config.ts          ✅ Config Tailwind
└── next.config.js              ✅ Config Next.js
```

---

## 🎨 Características Implementadas

### Componente BankBadge ⭐
```tsx
<BankBadge bank="SCOTIABANK" />  // Rojo
<BankBadge bank="BCP" />         // Azul oscuro
<BankBadge bank="FOGAPI" />      // Ámbar
<BankBadge bank={null} />        // Gris "Sin Garantía"
```

### Dashboard
- 4 KPI cards
- Gráfico de Top 5 Bancos
- Gráfico de Top 5 Entidades
- Diseño responsive

### Licitaciones
- Búsqueda con debounce
- Paginación del servidor
- Filtros sincronizados con URL
- Tabla responsive

### Detalle
- Layout 2/3 + 1/3
- Análisis de consorcios
- PieChart de distribución
- Información completa

---

## 🐛 Solución de Problemas

### Error: "npm no se reconoce"

**Solución:**
- Instalar Node.js desde: https://nodejs.org/
- Reiniciar PowerShell/CMD después de instalar

### Error: "Cannot find module"

**Solución:**
```bash
# Eliminar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Error: "Failed to fetch"

**Solución:**
1. Verificar que el backend esté corriendo en `http://localhost:8000`
2. Abrir DevTools del navegador (F12) y revisar la consola
3. Verificar CORS en el backend

### Puerto 3000 ocupado

**Solución:**
```bash
# Usar otro puerto
npm run dev -- -p 3001
```

---

## 📚 Documentación Adicional

- **README.md** - Documentación completa del proyecto
- **INSTALLATION.md** - Guía detallada de instalación
- **Walkthrough** - Explicación de toda la implementación

---

## 🎯 Próximos Pasos

1. ✅ Ejecutar `install.bat`
2. ✅ Ejecutar `start.bat`
3. ✅ Abrir `http://localhost:3000`
4. ✅ Explorar el Dashboard
5. ✅ Probar filtros en Licitaciones
6. ✅ Ver detalle de una licitación
7. ✅ Probar Dark Mode

---

## 💡 Tips

- **Hot Reload:** Los cambios en el código se reflejan automáticamente
- **DevTools:** Usa F12 para ver la consola y network
- **Dark Mode:** Botón en la esquina superior derecha
- **Sidebar:** Se puede colapsar para más espacio

---

**¡El frontend está listo para usar!** 🚀

Para cualquier duda, consulta la documentación completa en README.md
