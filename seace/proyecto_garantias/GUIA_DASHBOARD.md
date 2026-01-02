# 📊 Dashboard Web de Garantías SEACE

## 🎯 ¿Qué es esto?

Un dashboard web visual y profesional para explorar los datos de garantías SEACE de forma interactiva.

![Dashboard Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard+SEACE)

---

## ✨ Características

- ✅ **Estadísticas en tiempo real**: Total de licitaciones, adjudicaciones, garantías bancarias y retención
- ✅ **Filtros avanzados**: Buscar por texto, departamento, estado y tipo de garantía
- ✅ **Paginación**: Navega fácilmente entre miles de registros
- ✅ **Diseño responsive**: Se ve perfecto en desktop, tablet y móvil
- ✅ **Interfaz moderna**: Gradientes, animaciones y diseño profesional

---

## 🚀 Cómo Usar

### Paso 1: Instalar Dependencias

Necesitas instalar Flask y Flask-CORS:

```cmd
pip install flask flask-cors
```

### Paso 2: Iniciar la API

Abre una terminal y ejecuta:

```cmd
python api_dashboard.py
```

Deberías ver:
```
🚀 Iniciando API del Dashboard...
📊 API disponible en: http://localhost:5000
```

**IMPORTANTE**: Deja esta terminal abierta mientras uses el dashboard.

### Paso 3: Abrir el Dashboard

Abre el archivo `dashboard.html` en tu navegador:

**Opción A**: Doble clic en `dashboard.html`

**Opción B**: Desde el navegador:
- Chrome/Edge: `Ctrl + O` → Selecciona `dashboard.html`
- Firefox: `Ctrl + O` → Selecciona `dashboard.html`

---

## 🎨 Funcionalidades del Dashboard

### 1. **Tarjetas de Estadísticas**

En la parte superior verás 4 tarjetas con:
- 📋 Total de licitaciones
- ✅ Total de adjudicaciones
- 🏦 Garantías bancarias
- 💰 Garantías con retención

### 2. **Filtros de Búsqueda**

Puedes filtrar por:

- **Buscar**: ID de convocatoria, descripción o entidad
- **Departamento**: LIMA, CUSCO, AREQUIPA, etc.
- **Estado**: CONTRATADO, ADJUDICADO, CONSENTIDO, etc.
- **Tipo de Garantía**: Bancaria o Retención

**Ejemplo de búsqueda**:
```
Buscar: "hospital"
Departamento: LIMA
Estado: CONTRATADO
Tipo: BANCARIA
```

### 3. **Tabla de Resultados**

Muestra:
- ID de convocatoria
- Descripción del proyecto
- Entidad convocante
- Departamento
- Estado (con colores)
- Monto estimado
- Número de adjudicaciones
- Tipo de garantías

### 4. **Paginación**

- 20 registros por página
- Botones "Anterior" y "Siguiente"
- Indicador de página actual

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Buscar licitaciones en Lima con garantía bancaria

1. Selecciona **Departamento**: LIMA
2. Selecciona **Tipo de Garantía**: BANCARIA
3. Click en **Buscar**

### Ejemplo 2: Buscar proyectos de hospitales

1. Escribe en **Buscar**: "hospital"
2. Click en **Buscar**

### Ejemplo 3: Ver solo licitaciones contratadas

1. Selecciona **Estado**: CONTRATADO
2. Click en **Buscar**

---

## 🔧 Solución de Problemas

### Problema: "Error al cargar datos"

**Solución**: Asegúrate de que la API esté ejecutándose:
```cmd
python api_dashboard.py
```

### Problema: No aparecen datos

**Solución**: Verifica que la base de datos tenga datos:
```cmd
python comparar_con_oece.py
```

### Problema: CORS Error

**Solución**: Asegúrate de tener Flask-CORS instalado:
```cmd
pip install flask-cors
```

---

## 📊 API Endpoints

La API proporciona los siguientes endpoints:

### GET /api/stats
Obtiene estadísticas generales

**Respuesta**:
```json
{
  "total_licitaciones": 10043,
  "total_adjudicaciones": 7954,
  "garantias_bancarias": 3245,
  "garantias_retencion": 2845
}
```

### GET /api/licitaciones
Obtiene lista de licitaciones con filtros

**Parámetros**:
- `search`: Texto de búsqueda
- `departamento`: Departamento
- `estado`: Estado del proceso
- `tipo_garantia`: BANCARIA o RETENCION
- `page`: Número de página (default: 1)
- `per_page`: Registros por página (default: 20)

**Respuesta**:
```json
{
  "total": 1500,
  "page": 1,
  "per_page": 20,
  "total_pages": 75,
  "data": [...]
}
```

### GET /api/licitacion/<id>
Obtiene detalle de una licitación específica

### GET /api/filtros
Obtiene opciones para los filtros

---

## 🎨 Personalización

### Cambiar Colores

Edita `dashboard.html` y busca:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Cambia los colores por los que prefieras:
- `#667eea` → Color principal
- `#764ba2` → Color secundario

### Cambiar Registros por Página

En `api_dashboard.py`, línea 66:
```python
per_page = int(request.args.get('per_page', 20))  # Cambia 20 por el número que quieras
```

---

## 🚀 Próximas Mejoras (Futuro)

- [ ] Gráficas interactivas (Chart.js)
- [ ] Exportar a Excel/CSV
- [ ] Vista de detalle de cada licitación
- [ ] Mapa de calor por departamento
- [ ] Filtros por rango de fechas
- [ ] Filtros por monto
- [ ] Búsqueda avanzada con múltiples criterios

---

## 📝 Notas Técnicas

### Tecnologías Usadas

**Backend**:
- Flask (API REST)
- Flask-CORS (permitir peticiones desde el navegador)
- MySQL Connector (conexión a BD)

**Frontend**:
- HTML5
- CSS3 (con gradientes y animaciones)
- JavaScript Vanilla (sin frameworks)
- Fetch API (peticiones HTTP)

### Arquitectura

```
┌─────────────────┐
│  dashboard.html │  ← Frontend (navegador)
└────────┬────────┘
         │ HTTP Requests
         ↓
┌─────────────────┐
│ api_dashboard.py│  ← Backend (Flask)
└────────┬────────┘
         │ SQL Queries
         ↓
┌─────────────────┐
│  MySQL Database │  ← Base de datos
└─────────────────┘
```

---

## ✅ Checklist de Verificación

- [ ] Flask instalado (`pip install flask flask-cors`)
- [ ] API ejecutándose (`python api_dashboard.py`)
- [ ] Dashboard abierto en navegador
- [ ] Estadísticas cargando correctamente
- [ ] Filtros funcionando
- [ ] Tabla mostrando datos
- [ ] Paginación funcionando

---

**Creado**: 19 de diciembre de 2024  
**Versión**: 1.0  
**Estado**: ✅ Funcional
