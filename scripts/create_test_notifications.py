"""
Script para crear notificaciones de prueba
"""
import sys
sys.path.insert(0, 'c:/laragon/www/proyecto_garantias')

from app.database import SessionLocal
from app.services.notification_service import notification_service
from app.models.notification import NotificationType, NotificationPriority

db = SessionLocal()

print("🔔 Creando notificaciones de prueba...")

try:
    # Notificación de ALTA prioridad
    notification_service.create_notification(
        db=db,
        user_id=1,  # Asume usuario ID 1
        type=NotificationType.CARTA_FIANZA,
        priority=NotificationPriority.HIGH,
        title="⚠️ Carta Fianza próxima a vencer",
        message="La carta fianza #CF-2024-001 vence en 5 días. Se requiere acción inmediata para renovar o liberar.",
        link="/mqs/cartas-fianza",
        expires_days=7
    )
    print("✅ Notificación HIGH creada (Carta Fianza)")
    
    # Notificación de MEDIA prioridad
    notification_service.create_notification(
        db=db,
        user_id=1,
        type=NotificationType.ADJUDICACION,
        priority=NotificationPriority.MEDIUM,
        title="🏆 Nueva Adjudicación",
        message="La licitación 'Construcción Carretera Central' ha sido adjudicada a Consorcio ABC. Monto: S/ 5,200,000.",
        link="/seace/database",
        expires_days=30
    )
    print("✅ Notificación MEDIUM creada (Adjudicación)")
    
    # Notificación de BAJA prioridad
    notification_service.create_notification(
        db=db,
        user_id=1,
        type=NotificationType.REPORTE,
        priority=NotificationPriority.LOW,
        title="📊 Reporte mensual disponible",
        message="El reporte de análisis de licitaciones de Diciembre 2024 está listo para su revisión.",
        link="/seace/tendencias",
        expires_days=30
    )
    print("✅ Notificación LOW creada (Reporte)")
    
    # Notificación de Sistema
    notification_service.create_notification(
        db=db,
        user_id=1,
        type=NotificationType.SISTEMA,
        priority=NotificationPriority.LOW,
        title="⚙️ Nueva funcionalidad disponible",
        message="El asistente AI ahora incluye sugerencias contextuales y sistema de aprendizaje. ¡Pruébalo!",
        link="/settings",
        expires_days=30
    )
    print("✅ Notificación SISTEMA creada")
    
    # Notificación de Licitación
    notification_service.create_notification(
        db=db,
        user_id=1,
        type=NotificationType.LICITACION,
        priority=NotificationPriority.MEDIUM,
        title="📋 Licitación próxima a cerrar",
        message="La licitación 'Suministro de Equipos Médicos' cierra en 24 horas. Monto estimado: S/ 850,000.",
        link="/seace/database",
        expires_days=15
    )
    print("✅ Notificación LICITACION creada")
    
    print(f"\n🎉 Se crearon 5 notificaciones de prueba exitosamente!")
    print(f"💡 Ve a http://localhost:3000 y verifica el ícono de campana en el header")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
