"""
SCRIPT DE CORRECCION AUTOMATICA
Corrige todos los problemas detectados en la auditoria
"""
import mysql.connector
from config.secrets_manager import get_db_config
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("=" * 100)
print(" CORRECCION AUTOMATICA DE PROBLEMAS")
print("=" * 100)

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

# ============================================================================
# CORRECCION 1: Limpiar RUCs con prefijo PE-RUC-
# ============================================================================
print("\n1. Limpiando RUCs con prefijo PE-RUC-...")

cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_ruc LIKE 'PE-RUC-%'")
total_antes = cursor.fetchone()[0]
print(f"   RUCs con prefijo antes: {total_antes:,}")

cursor.execute("""
    UPDATE Licitaciones_Adjudicaciones 
    SET ganador_ruc = REPLACE(ganador_ruc, 'PE-RUC-', '')
    WHERE ganador_ruc LIKE 'PE-RUC-%'
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_ruc LIKE 'PE-RUC-%'")
total_despues = cursor.fetchone()[0]

print(f"   RUCs con prefijo despues: {total_despues:,}")
print(f"   OK - Corregidos {total_antes - total_despues:,} RUCs")

# ============================================================================
# CORRECCION 2: Eliminar adjudicaciones huerfanas
# ============================================================================
print("\n2. Eliminando adjudicaciones huerfanas...")

cursor.execute("""
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones a
    LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE c.id_convocatoria IS NULL
""")
total_huerfanas = cursor.fetchone()[0]
print(f"   Adjudicaciones huerfanas: {total_huerfanas:,}")

if total_huerfanas > 0:
    cursor.execute("""
        DELETE a FROM Licitaciones_Adjudicaciones a
        LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
        WHERE c.id_convocatoria IS NULL
    """)
    conn.commit()
    print(f"   OK - Eliminadas {total_huerfanas:,} adjudicaciones huerfanas")
else:
    print(f"   OK - No hay adjudicaciones huerfanas")

# ============================================================================
# CORRECCION 3: Eliminar contratos huerfanos
# ============================================================================
print("\n3. Eliminando contratos huerfanos...")

cursor.execute("""
    SELECT COUNT(*) 
    FROM Contratos c
    LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_adjudicacion = a.id_adjudicacion
    WHERE a.id_adjudicacion IS NULL
""")
total_cont_huerfanos = cursor.fetchone()[0]
print(f"   Contratos huerfanos: {total_cont_huerfanos:,}")

if total_cont_huerfanos > 0:
    cursor.execute("""
        DELETE c FROM Contratos c
        LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_adjudicacion = a.id_adjudicacion
        WHERE a.id_adjudicacion IS NULL
    """)
    conn.commit()
    print(f"   OK - Eliminados {total_cont_huerfanos:,} contratos huerfanos")
else:
    print(f"   OK - No hay contratos huerfanos")

# ============================================================================
# VERIFICACION FINAL
# ============================================================================
print("\n" + "=" * 100)
print(" VERIFICACION FINAL")
print("=" * 100)

# Verificar RUCs
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones WHERE ganador_ruc LIKE 'PE-RUC-%'")
rucs_prefijo = cursor.fetchone()[0]
print(f"\n1. RUCs con prefijo: {rucs_prefijo:,}")
if rucs_prefijo == 0:
    print(f"   OK - Todos los RUCs limpiados")
else:
    print(f"   ERROR - Aun quedan {rucs_prefijo:,} RUCs con prefijo")

# Verificar huerfanos
cursor.execute("""
    SELECT COUNT(*) 
    FROM Licitaciones_Adjudicaciones a
    LEFT JOIN Licitaciones_Cabecera c ON a.id_convocatoria = c.id_convocatoria
    WHERE c.id_convocatoria IS NULL
""")
adj_huerfanas = cursor.fetchone()[0]
print(f"\n2. Adjudicaciones huerfanas: {adj_huerfanas:,}")
if adj_huerfanas == 0:
    print(f"   OK - No hay adjudicaciones huerfanas")

cursor.execute("""
    SELECT COUNT(*) 
    FROM Contratos c
    LEFT JOIN Licitaciones_Adjudicaciones a ON c.id_adjudicacion = a.id_adjudicacion
    WHERE a.id_adjudicacion IS NULL
""")
cont_huerfanos = cursor.fetchone()[0]
print(f"\n3. Contratos huerfanos: {cont_huerfanos:,}")
if cont_huerfanos == 0:
    print(f"   OK - No hay contratos huerfanos")

# Estadisticas finales
cursor.execute("SELECT COUNT(*) FROM Licitaciones_Cabecera")
total_lic = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Licitaciones_Adjudicaciones")
total_adj = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Contratos")
total_cont = cursor.fetchone()[0]

print("\n" + "=" * 100)
print(" ESTADISTICAS FINALES")
print("=" * 100)
print(f"\nLicitaciones_Cabecera:       {total_lic:,}")
print(f"Licitaciones_Adjudicaciones: {total_adj:,}")
print(f"Contratos:                   {total_cont:,}")

print("\n" + "=" * 100)
print(" CORRECCIONES COMPLETADAS")
print("=" * 100)

conn.close()
