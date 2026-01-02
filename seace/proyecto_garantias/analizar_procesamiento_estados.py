# Script para analizar cómo se procesan los estados del JSON
import json
import os

# Simular la función actual
def determinar_estado_actual(tender_status, item_status):
    """Función ACTUAL del cargador.py"""
    def safe_str(val):
        if val is None: return ""
        return str(val).strip()
    
    st_item = safe_str(item_status)
    if st_item: return st_item.upper()
    
    st = safe_str(tender_status).lower()
    if not st: return "DESCONOCIDO"

    mapping = {
        'active': 'CONVOCADO', 
        'complete': 'CONTRATADO', 
        'cancelled': 'CANCELADO', 
        'unsuccessful': 'DESIERTO', 
        'withdrawn': 'NULO', 
        'planned': 'PROGRAMADO', 
        'awarded': 'ADJUDICADO'
    }
    return mapping.get(st, st.upper())

# Función propuesta (sin traducciones)
def determinar_estado_propuesto(tender_status, item_status):
    """Función PROPUESTA - Sin traducciones, valores originales"""
    def safe_str(val):
        if val is None: return ""
        return str(val).strip()
    
    # Priorizar estado del item si existe
    st_item = safe_str(item_status)
    if st_item: return st_item.upper()
    
    # Si no hay estado de item, usar estado del tender
    st = safe_str(tender_status)
    if not st: return "DESCONOCIDO"
    
    # Retornar el valor ORIGINAL en mayúsculas, sin traducciones
    return st.upper()

print("=" * 80)
print("ANALISIS: PROCESAMIENTO DE ESTADOS")
print("=" * 80)

# Ejemplos de estados del JSON SEACE
ejemplos_json = [
    ('active', None),
    ('complete', None),
    ('awarded', None),
    ('cancelled', None),
    ('unsuccessful', None),
    ('withdrawn', None),
    ('planned', None),
    ('ADJUDICADO', None),
    ('CONSENTIDO', None),
    ('CONTRATADO', None),
    ('RETROTRAID_POR_RESOLUCION', None),
    ('APELADO', None),
    ('DESIERTO', None),
    ('NULO', None),
]

print("\n1. COMPARACION: FUNCION ACTUAL vs PROPUESTA")
print("-" * 80)
print(f"{'JSON tender.status':<35} {'ACTUAL (Traducido)':<25} {'PROPUESTO (Original)':<25}")
print("-" * 80)

for tender_status, item_status in ejemplos_json:
    actual = determinar_estado_actual(tender_status, item_status)
    propuesto = determinar_estado_propuesto(tender_status, item_status)
    
    diferente = "[!]" if actual != propuesto else "[OK]"
    print(f"{tender_status:<35} {actual:<25} {propuesto:<25} {diferente}")

print("\n\n2. PROBLEMA IDENTIFICADO")
print("-" * 80)
print("""
La función ACTUAL hace TRADUCCIONES de inglés a español:
- 'active' → 'CONVOCADO'
- 'complete' → 'CONTRATADO'
- 'awarded' → 'ADJUDICADO'
- etc.

Esto causa INCONSISTENCIAS porque:
1. El JSON del SEACE puede tener estados en ESPAÑOL o INGLÉS
2. La traducción solo funciona para estados en inglés
3. Estados ya en español se quedan como están
4. Resultado: Base de datos con mezcla de formatos

SOLUCION: Guardar el valor ORIGINAL sin traducciones
""")

print("\n3. VENTAJAS DE USAR VALORES ORIGINALES")
print("-" * 80)
print("""
[OK] CONSISTENCIA: Todos los estados como vienen del SEACE
[OK] TRAZABILIDAD: Facil comparar BD con JSON original
[OK] ACTUALIZACIONES: Si SEACE cambia estados, se reflejan automaticamente
[OK] SIN ERRORES: No hay riesgo de traducciones incorrectas
[OK] MANTENIBILIDAD: Codigo mas simple, sin diccionario de traducciones
""")

print("\n4. DESVENTAJAS (MINIMAS)")
print("-" * 80)
print("""
[!] Estados en ingles: Algunos estados estaran en ingles (active, complete, etc.)
   SOLUCION: Crear vista SQL o funcion para traducir al consultar

[!] Mayusculas/minusculas: Pueden venir en diferentes formatos
   SOLUCION: Normalizar a MAYUSCULAS al guardar (ya se hace)
""")

print("\n5. RECOMENDACION")
print("-" * 80)
print("""
OPCION 1 (RECOMENDADA): Guardar valores ORIGINALES
- Modificar función determinar_estado() para NO traducir
- Guardar exactamente como viene en JSON
- Crear vista SQL para traducción si es necesario

OPCION 2: Mantener traducciones pero COMPLETAS
- Ampliar diccionario con TODOS los estados posibles
- Incluir estados en español también
- Riesgo: Puede quedar incompleto si SEACE agrega nuevos estados

OPCION 3: Híbrido
- Guardar valor original en una columna
- Guardar valor traducido en otra columna
- Más espacio pero máxima flexibilidad
""")

print("\n" + "=" * 80)
print("ANALISIS COMPLETADO")
print("=" * 80)
