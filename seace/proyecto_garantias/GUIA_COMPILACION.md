# 🏗️ Guía de Compilación - Sistema SEACE

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Compilación Completa](#compilación-completa)
3. [Modos de Ejecución](#modos-de-ejecución)
4. [Comandos Manuales](#comandos-manuales)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos Previos

Antes de compilar, asegúrate de tener instalado:

- ✅ **Node.js** v18 o superior ([Descargar](https://nodejs.org/))
- ✅ **npm** (incluido con Node.js)
- ✅ **MySQL** (incluido en Laragon)
- ✅ **Git** (opcional, para control de versiones)

### Verificar instalación:

```cmd
node --version
npm --version
```

---

## 🚀 Compilación Completa

### Opción 1: Script Automático (Recomendado)

```cmd
compilar_proyecto.bat
```

Este script:
1. ✅ Instala dependencias del backend
2. ✅ Instala dependencias del frontend
3. ✅ Compila el frontend (Vite build)
4. ✅ Genera archivos optimizados en `frontend/dist`

### Opción 2: Manual

#### Backend:
```cmd
cd backend
npm install
```

#### Frontend:
```cmd
cd frontend
npm install
npm run build
```

---

## 🎯 Modos de Ejecución

### Script Interactivo (Recomendado)

```cmd
iniciar_proyecto.bat
```

Opciones disponibles:

#### 1️⃣ Modo DESARROLLO
- **Backend**: Hot-reload con nodemon (puerto 5000)
- **Frontend**: Hot-reload con Vite (puerto 5173)
- **Ideal para**: Desarrollo activo, cambios en tiempo real

```cmd
# Backend: http://localhost:5000
# Frontend: http://localhost:5173
```

#### 2️⃣ Modo PRODUCCIÓN
- **Backend**: Node.js optimizado (puerto 5000)
- **Frontend**: Archivos compilados servidos desde `dist/`
- **Ideal para**: Testing de producción, demos

#### 3️⃣ Solo BACKEND
- Inicia únicamente el servidor API
- **Puerto**: 5000

#### 4️⃣ Solo FRONTEND
- Inicia únicamente la interfaz de usuario
- **Puerto**: 5173

---

## 📝 Comandos Manuales

### Backend

```cmd
cd backend

# Desarrollo (con auto-reload)
npm run dev

# Producción
npm start
```

### Frontend

```cmd
cd frontend

# Desarrollo (con hot-reload)
npm run dev

# Compilar para producción
npm run build

# Preview del build
npm run preview
```

---

## 🗂️ Estructura de Archivos Compilados

```
proyecto_garantias/
├── backend/
│   ├── node_modules/      # Dependencias backend
│   ├── server.js          # Servidor principal
│   └── package.json
│
├── frontend/
│   ├── node_modules/      # Dependencias frontend
│   ├── dist/              # ⭐ ARCHIVOS COMPILADOS
│   │   ├── index.html
│   │   ├── assets/
│   │   │   ├── index-[hash].js
│   │   │   └── index-[hash].css
│   │   └── ...
│   ├── src/               # Código fuente
│   └── package.json
│
└── compilar_proyecto.bat  # Script de compilación
```

---

## 🔍 Verificación Post-Compilación

### 1. Verificar archivos compilados:

```cmd
dir frontend\dist
```

Deberías ver:
- ✅ `index.html`
- ✅ Carpeta `assets/` con archivos JS y CSS

### 2. Verificar tamaño del build:

```cmd
cd frontend
npm run build
```

Salida esperada:
```
✓ built in [tiempo]
dist/index.html                   [tamaño]
dist/assets/index-[hash].js       [tamaño]
dist/assets/index-[hash].css      [tamaño]
```

### 3. Probar el build localmente:

```cmd
cd frontend
npm run preview
```

Abre: http://localhost:4173

---

## ⚠️ Solución de Problemas

### ❌ Error: "npm no se reconoce como comando"

**Solución**: Instala Node.js desde https://nodejs.org/

### ❌ Error: "Cannot find module"

**Solución**: Reinstala dependencias
```cmd
# Backend
cd backend
rmdir /s /q node_modules
npm install

# Frontend
cd frontend
rmdir /s /q node_modules
npm install
```

### ❌ Error: "Port 5000 already in use"

**Solución**: Cambia el puerto en `backend/.env`
```env
PORT=5001
```

### ❌ Error: "ECONNREFUSED" al conectar a MySQL

**Solución**: 
1. Verifica que MySQL esté corriendo en Laragon
2. Revisa credenciales en `backend/.env`
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=seace_garantias
```

### ❌ Frontend compilado muestra página en blanco

**Solución**: Verifica la configuración de Vite

`frontend/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './', // Importante para rutas relativas
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
})
```

### ❌ Error: "Out of memory" durante build

**Solución**: Aumenta memoria de Node.js
```cmd
set NODE_OPTIONS=--max-old-space-size=4096
npm run build
```

---

## 📊 Optimización del Build

### Reducir tamaño del bundle:

1. **Analizar el bundle**:
```cmd
cd frontend
npm install --save-dev rollup-plugin-visualizer
```

2. **Lazy loading de componentes**:
```javascript
// Antes
import Dashboard from './pages/Dashboard';

// Después
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

3. **Code splitting**:
```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'chart-vendor': ['chart.js', 'react-chartjs-2']
        }
      }
    }
  }
})
```

---

## 🚀 Despliegue

### Opción 1: Servidor Local (Laragon)

1. Compila el frontend:
```cmd
cd frontend
npm run build
```

2. Configura Apache/Nginx para servir `frontend/dist`

3. Inicia el backend:
```cmd
cd backend
npm start
```

### Opción 2: Servidor Remoto

1. Sube los archivos:
   - `backend/` completo
   - `frontend/dist/` (solo archivos compilados)

2. En el servidor:
```bash
cd backend
npm install --production
npm start
```

3. Configura reverse proxy (Nginx):
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        root /ruta/a/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

---

## 📚 Recursos Adicionales

- [Documentación de Vite](https://vitejs.dev/)
- [Documentación de Express](https://expressjs.com/)
- [Guía de React](https://react.dev/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)

---

## 🆘 Soporte

Si encuentras problemas:

1. ✅ Revisa esta guía
2. ✅ Verifica los logs en consola
3. ✅ Ejecuta `diagnostico.bat` para análisis automático
4. ✅ Revisa `backend/.env` y configuraciones

---

**Última actualización**: 19 de diciembre de 2024  
**Versión**: 2.0
