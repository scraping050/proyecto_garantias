"""
Script para limpiar control de cargas y re-ejecutar ETL
"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace'
)

cursor = conn.cursor()

print("=" * 100)
print("LIMPIANDO CONTROL DE CARGAS PARA RE-PROCESAR")
print("=" * 100)

# Limpiar control_cargas
cursor.execute("DELETE FROM control_cargas")
conn.commit()

print("\nOK - Control de cargas limpiado")
print("Ahora puedes ejecutar: python 1_motor_etl\\cargador.py")

cursor.close()
conn.close()

print("\n" + "=" * 100)
