# Script para crear la base de datos garantias_seace
import mysql.connector

try:
    # Conectar sin especificar base de datos
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789'
    )
    
    cursor = conn.cursor()
    
    # Crear base de datos
    cursor.execute("CREATE DATABASE IF NOT EXISTS garantias_seace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("OK - Base de datos 'garantias_seace' creada exitosamente")
    
    # Verificar que existe
    cursor.execute("SHOW DATABASES LIKE 'garantias_seace'")
    result = cursor.fetchone()
    if result:
        print("OK - Base de datos verificada")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
