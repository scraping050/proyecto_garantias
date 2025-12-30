"""
Script para crear notificaciones de prueba en el sistema
"""
from app.database import SessionLocal
from app.models.notification import Notification, NotificationType, NotificationPriority
from datetime import datetime, timezone, timedelta

def create_sample_notifications():
    db = SessionLocal()
    
    try:
        # Obtener el ID del primer usuario
        from app.models.user import User
        first_user = db.query(User).first()
        
        if not first_user:
            print("No hay usuarios en la base de datos. Crea un usuario primero.")
            return
        
        user_id = first_user.id
        print(f"Creando notificaciones para usuario: {first_user.username} (ID: {user_id})")
        
        # Limpiar notificaciones antiguas (opcional)
        db.query(Notification).delete()
        
        # Notificaciones de prueba
        notifications_data = [
            {
                "type": NotificationType.LICITACION,
                "priority": NotificationPriority.HIGH,
                "title": "Nueva Licitación Publicada",
                "message": "Se ha publicado una nueva licitación en la categoría OBRAS por un monto de S/ 2,350,000",
                "link": "/seace/busqueda"
            },
            {
                "type": NotificationType.CARTA_FIANZA,
                "priority": NotificationPriority.MEDIUM,
                "title": "Carta Fianza próxima a vencer",
                "message": "La carta fianza #CF-2024-001 vencerá en 15 días",
                "link": "/mqs/fianzas"
            },
            {
                "type": NotificationType.ADJUDICACION,
                "priority": NotificationPriority.HIGH,
                "title": "Adjudicación Confirmada",
                "message": "Se ha confirmado la adjudicación de la licitación ADJ-2024-0045",
                "link": "/seace/licitaciones/12345"
            },
            {
                "type": NotificationType.REPORTE,
                "priority": NotificationPriority.LOW,
                "title": "Reporte Mensual Generado",
                "message": "El reporte de garantías del mes de Diciembre está disponible",
                "link": "/seace/reportes"
            },
            {
                "type": NotificationType.SISTEMA,
                "priority": NotificationPriority.MEDIUM,
                "title": "Actualización del Sistema",
                "message": "El sistema se actualizó a la versión 3.0.0 con nuevas funcionalidades",
                "link": null
            },
            {
                "type": NotificationType.CONSORCIO,
                "priority": NotificationPriority.LOW,
                "title": "Nuevo Consorcio Registrado",
                "message": "Se ha registrado un nuevo consorcio: 'Constructora Unidos SAC'",
                "link": "/mqs/obras"
            },
            {
                "type": NotificationType.LICITACION,
                "priority": NotificationPriority.MEDIUM,
                "title": "Licitación en Estado ADJUDICADO",
                "message": "La licitación LIC-2024-0234 cambió a estado ADJUDICADO",
                "link": "/seace/busqueda"
            },
        ]
        
        created_notifications = []
        for notif_data in notifications_data:
            notification = Notification(
                user_id=user_id,
                type=notif_data["type"],
                priority=notif_data["priority"],
                title=notif_data["title"],
                message=notif_data["message"],
                link=notif_data["link"],
                is_read=False,
                expires_at=datetime.now(timezone.utc) + timedelta(days=30)
            )
            db.add(notification)
            created_notifications.append(notification)
        
        db.commit()
        
        print(f"\n✅ Se crearon {len(created_notifications)} notificaciones de prueba exitosamente!")
        print("\nNotificaciones creadas:")
        for notif in created_notifications:
            priority_emoji = "🔴" if notif.priority == NotificationPriority.HIGH else "🟡" if notif.priority == NotificationPriority.MEDIUM else "🔵"
            print(f"  {priority_emoji} [{notif.type.value.upper()}] {notif.title}")
        
        print(f"\n📊 Total de notificaciones en BD: {db.query(Notification).count()}")
        print(f"📨 Notificaciones no leídas: {db.query(Notification).filter_by(is_read=False).count()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_notifications()
