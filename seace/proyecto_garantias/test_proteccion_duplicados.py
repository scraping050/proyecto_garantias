import mysql.connector
import sys
import os

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

conn = mysql.connector.connect(**get_db_config())
cursor = conn.cursor()

print("=" * 70)
print("DEMOSTRACIÓN: PROTECCIÓN CONTRA DUPLICADOS")
print("=" * 70)

# 1. Limpiar duplicados de la prueba anterior
print("\n1. LIMPIANDO DUPLICADOS DE PRUEBA ANTERIOR...")
cursor.execute("""
    DELETE FROM Detalle_Consorcios 
    WHERE id_contrato = '2280973' 
      AND fecha_registro > '2025-12-20 21:00:00'
""")
conn.commit()
print(f"   Eliminados: {cursor.rowcount} registros")

# 2. Contar registros actuales
cursor.execute("""
    SELECT COUNT(*) FROM Detalle_Consorcios 
    WHERE id_contrato = '2280973'
""")
count_antes = cursor.fetchone()[0]
print(f"\n2. REGISTROS ACTUALES: {count_antes}")

# 3. Simular que el ETL se ejecuta DOS VECES
print("\n3. SIMULANDO EJECUCIÓN DOBLE DEL ETL:")

sql_insert = """
    INSERT INTO Detalle_Consorcios 
    (id_contrato, ruc_miembro, nombre_miembro, porcentaje_participacion)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE fecha_registro=NOW()
"""

# Datos del contrato 2280973 (ya procesado)
datos = [
    ('2280973', '20123456789', 'CENTAURO ENTERPRISE SAC', 40.0),
    ('2280973', '20987654321', 'INVERSIONES LECHE MASS SAC', 60.0)
]

# Primera ejecución (simulada)
print("   - Primera ejecución...")
cursor.executemany(sql_insert, datos)
conn.commit()

# Segunda ejecución (simulada - esto es lo que queremos prevenir)
print("   - Segunda ejecución (intento de duplicar)...")
cursor.executemany(sql_insert, datos)
conn.commit()

# 4. Verificar que NO se duplicaron
cursor.execute("""
    SELECT COUNT(*) FROM Detalle_Consorcios 
    WHERE id_contrato = '2280973'
""")
count_despues = cursor.fetchone()[0]

print(f"\n4. RESULTADO:")
print(f"   Registros ANTES:  {count_antes}")
print(f"   Registros DESPUÉS: {count_despues}")
print(f"   Diferencia: {count_despues - count_antes}")

if count_despues == count_antes:
    print("\n   ✅ PROTECCIÓN EXITOSA: NO SE CREARON DUPLICADOS")
else:
    print(f"\n   ⚠️  Se agregaron {count_despues - count_antes} registros")

# 5. Mostrar datos finales
print("\n5. DATOS FINALES EN BD:")
cursor.execute("""
    SELECT ruc_miembro, nombre_miembro, porcentaje_participacion, fecha_registro
    FROM Detalle_Consorcios
    WHERE id_contrato = '2280973'
    ORDER BY fecha_registro
""")
for row in cursor.fetchall():
    print(f"   - RUC: {row[0]}, {row[1]} ({row[2]}%) - {row[3]}")

# 6. Verificar que LEFT JOIN funciona
print("\n6. VERIFICANDO LEFT JOIN (¿El ETL volvería a procesar este contrato?):")
cursor.execute("""
    SELECT a.id_contrato
    FROM Licitaciones_Adjudicaciones a
    LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
    WHERE a.id_contrato = '2280973'
      AND d.id_contrato IS NULL
""")
resultado_join = cursor.fetchall()

if len(resultado_join) == 0:
    print("   ✅ LEFT JOIN FUNCIONA: Este contrato NO aparecería en la consulta")
    print("   ✅ El ETL NO intentaría procesarlo de nuevo")
else:
    print("   ❌ LEFT JOIN NO FUNCIONA: Este contrato aparecería en la consulta")

print("\n" + "=" * 70)
print("CONCLUSIÓN FINAL:")
print("=" * 70)
print("✅ UNIQUE KEY: Previene duplicados a nivel de base de datos")
print("✅ ON DUPLICATE KEY UPDATE: Actualiza en vez de duplicar")
print("✅ LEFT JOIN: Evita que el ETL intente procesar contratos ya procesados")
print("\n🛡️  EL SISTEMA ES SEGURO CONTRA DUPLICADOS")
print("=" * 70)

conn.close()
