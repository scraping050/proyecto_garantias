# Guía de Instalación - SEACE Monitor Frontend

## 📋 Comandos de Instalación Paso a Paso

### 1. Navegar al Directorio del Frontend

```bash
cd c:\laragon\www\proyecto_garantias\frontend
```

### 2. Instalar Dependencias Base

```bash
npm install
```

Esto instalará todas las dependencias listadas en `package.json`:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- TanStack Query
- Recharts
- Lucide React (iconos)
- Radix UI primitives
- date-fns
- clsx y tailwind-merge

### 3. Instalar Dependencia Adicional (tailwindcss-animate)

```bash
npm install tailwindcss-animate
```

### 4. Instalar next-themes para Dark Mode

```bash
npm install next-themes
```

### 5. Verificar Instalación

```bash
npm list
```

Deberías ver todas las dependencias instaladas sin errores.

### 6. Ejecutar en Modo Desarrollo

```bash
npm run dev
```

El servidor se iniciará en: **http://localhost:3000**

---

## 🎨 Instalación de Componentes Shadcn UI (Opcional)

Si necesitas agregar más componentes de Shadcn UI en el futuro, usa estos comandos:

```bash
# Componentes ya incluidos en el proyecto:
npx shadcn-ui@latest add button
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input

# Componentes adicionales disponibles:
npx shadcn-ui@latest add table
npx shadcn-ui@latest add select
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add popover
npx shadcn-ui@latest add calendar
npx shadcn-ui@latest add command
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add sheet
npx shadcn-ui@latest add hover-card
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add skeleton
```

**Nota:** Los componentes básicos ya están incluidos en el código fuente del proyecto.

---

## ✅ Verificación de Instalación

### 1. Verificar que el Backend esté corriendo

```bash
# En otra terminal, navega al backend
cd c:\laragon\www\proyecto_garantias
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Verificar que el Frontend esté corriendo

```bash
# En la terminal del frontend
npm run dev
```

### 3. Abrir el navegador

Navega a: **http://localhost:3000**

Deberías ver:
- ✅ Sidebar con navegación
- ✅ Dashboard con KPIs
- ✅ Gráficos de Recharts
- ✅ Tema claro/oscuro funcional

---

## 🔧 Solución de Problemas

### Error: "Cannot find module 'next'"

**Solución:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Error: "Module not found: Can't resolve '@/components/...'"

**Solución:**
Verifica que `tsconfig.json` tenga:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### Error: "Failed to fetch" en el navegador

**Solución:**
1. Verifica que el backend esté corriendo en `http://localhost:8000`
2. Verifica CORS en el backend
3. Abre las DevTools del navegador y revisa la consola

### Estilos de Tailwind no se aplican

**Solución:**
1. Verifica que `globals.css` esté importado en `layout.tsx`
2. Ejecuta:
```bash
npm run dev
```
3. Limpia el cache del navegador (Ctrl + Shift + R)

---

## 📦 Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| next | ^14.1.0 | Framework React |
| react | ^18.2.0 | Biblioteca UI |
| typescript | ^5.3.3 | Tipado estático |
| tailwindcss | ^3.4.1 | Estilos utility-first |
| @tanstack/react-query | ^5.17.19 | Data fetching y caching |
| recharts | ^2.10.3 | Gráficos y visualizaciones |
| lucide-react | ^0.309.0 | Iconos |
| next-themes | latest | Dark mode |
| tailwindcss-animate | latest | Animaciones |

---

## 🚀 Comandos Útiles

```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Ejecutar build de producción
npm run start

# Linter
npm run lint

# Limpiar cache de Next.js
rm -rf .next

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

---

## 📝 Próximos Pasos

Después de la instalación:

1. ✅ Verifica que el Dashboard cargue correctamente
2. ✅ Prueba la navegación a Licitaciones
3. ✅ Prueba los filtros y la paginación
4. ✅ Abre una licitación en detalle
5. ✅ Prueba el toggle de Dark Mode
6. ✅ Verifica que los gráficos se rendericen

---

**¡Instalación Completa!** 🎉

El frontend está listo para usar. Consulta el [README.md](./README.md) para más información sobre el uso y la arquitectura del proyecto.
