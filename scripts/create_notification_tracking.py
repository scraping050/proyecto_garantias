"""
Script para crear tabla notification_tracking
"""
import sys
sys.path.insert(0, 'c:/laragon/www/proyecto_garantias')

from sqlalchemy import text
from app.database import SessionLocal

db = SessionLocal()

try:
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS notification_tracking (
            id INT PRIMARY KEY AUTO_INCREMENT,
            entity_type VARCHAR(50),
            entity_id VARCHAR(100),
            notification_type VARCHAR(50),
            last_notified TIMESTAMP,
            INDEX idx_entity (entity_type, entity_id)
        )
    """))
    db.commit()
    print("✅ Tabla notification_tracking creada exitosamente")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
