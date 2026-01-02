"""
Script para configurar el sistema de notificaciones
Crea la tabla de notificaciones y el trigger para detectar cambios de estado
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def setup_notifications():
    connection = None
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', '123456789'),
            database='garantias_seace'  # Base de datos correcta
        )
        
        cursor = connection.cursor()
        
        print("=" * 60)
        print("🔔 CONFIGURANDO SISTEMA DE NOTIFICACIONES")
        print("=" * 60)
        
        # Crear tabla de notificaciones
        print("\n📋 Creando tabla 'notificaciones'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificaciones (
              id INT AUTO_INCREMENT PRIMARY KEY,
              id_convocatoria VARCHAR(100) NOT NULL,
              tipo VARCHAR(50) NOT NULL DEFAULT 'CAMBIO_ESTADO',
              titulo VARCHAR(255) NOT NULL,
              mensaje TEXT NOT NULL,
              estado_anterior VARCHAR(100),
              estado_nuevo VARCHAR(100),
              leida BOOLEAN DEFAULT FALSE,
              fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              fecha_lectura TIMESTAMP NULL,
              metadata JSON,
              INDEX idx_convocatoria (id_convocatoria),
              INDEX idx_leida (leida),
              INDEX idx_fecha (fecha_creacion DESC),
              FOREIGN KEY (id_convocatoria) REFERENCES licitaciones_cabecera(id_convocatoria) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Tabla 'notificaciones' creada exitosamente")
        
        # Eliminar trigger si existe
        print("\n🗑️  Eliminando trigger anterior (si existe)...")
        try:
            cursor.execute("DROP TRIGGER IF EXISTS notificar_cambio_estado")
            print("✅ Trigger anterior eliminado")
        except:
            print("ℹ️  No había trigger anterior")
        
        # Crear trigger
        print("\n⚡ Creando trigger 'notificar_cambio_estado'...")
        cursor.execute("""
            CREATE TRIGGER notificar_cambio_estado
            AFTER UPDATE ON licitaciones_cabecera
            FOR EACH ROW
            BEGIN
              -- Solo crear notificación si el estado cambió
              IF OLD.estado_proceso != NEW.estado_proceso OR 
                 (OLD.estado_proceso IS NULL AND NEW.estado_proceso IS NOT NULL) OR 
                 (OLD.estado_proceso IS NOT NULL AND NEW.estado_proceso IS NULL) THEN
                INSERT INTO notificaciones (
                  id_convocatoria,
                  tipo,
                  titulo,
                  mensaje,
                  estado_anterior,
                  estado_nuevo,
                  metadata
                ) VALUES (
                  NEW.id_convocatoria,
                  'CAMBIO_ESTADO',
                  CONCAT('Cambio de estado: ', SUBSTRING(NEW.descripcion, 1, 100)),
                  CONCAT('La licitación "', SUBSTRING(NEW.descripcion, 1, 150), '" cambió de estado de "', 
                         COALESCE(OLD.estado_proceso, 'SIN ESTADO'), '" a "', 
                         COALESCE(NEW.estado_proceso, 'SIN ESTADO'), '"'),
                  OLD.estado_proceso,
                  NEW.estado_proceso,
                  JSON_OBJECT(
                    'comprador', NEW.comprador,
                    'monto_estimado', NEW.monto_estimado,
                    'departamento', NEW.departamento,
                    'categoria', NEW.categoria
                  )
                );
              END IF;
            END
        """)
        print("✅ Trigger 'notificar_cambio_estado' creado exitosamente")
        
        connection.commit()
        
        # Verificar creación
        print("\n🔍 Verificando configuración...")
        cursor.execute("SHOW TABLES LIKE 'notificaciones'")
        if cursor.fetchone():
            print("✅ Tabla 'notificaciones' existe")
        
        cursor.execute("SHOW TRIGGERS LIKE 'licitaciones_cabecera'")
        triggers = cursor.fetchall()
        if triggers:
            print(f"✅ Trigger configurado: {triggers[0][0]}")
        
        print("\n" + "=" * 60)
        print("✅ SISTEMA DE NOTIFICACIONES CONFIGURADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📝 Próximos pasos:")
        print("   1. El trigger detectará automáticamente cambios de estado")
        print("   2. Las notificaciones aparecerán en /notificaciones")
        print("   3. El contador se mostrará en el header")
        print("\n🧪 Para probar, actualiza el estado de una licitación:")
        print("   UPDATE licitaciones_cabecera SET estado_proceso = 'NULO'")
        print("   WHERE id_convocatoria = 'tu-id' AND estado_proceso = 'CONTRATADO';")
        print()
        
    except mysql.connector.Error as error:
        print(f"\n❌ Error: {error}")
        return False
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == "__main__":
    setup_notifications()
