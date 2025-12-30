"""
Notifications Router - API endpoints para notificaciones (RECREADO CORRECTAMENTE)
"""
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.notification_service import notification_service
from app.models.notification import NotificationType, NotificationPriority
from app.schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationList,
    UnreadCountResponse
)
from app.utils.dependencies import get_current_user, SECRET_KEY, ALGORITHM
from app.models.user import User
from app.websocket_manager import manager
import jwt

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("/", response_model=NotificationList)
def get_notifications(
    unread_only: bool = False,
    type_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener notificaciones del usuario actual con filtros opcionales"""
    notifications = notification_service.get_user_notifications(
        db=db,
        user_id=current_user.id,
        unread_only=unread_only,
        type_filter=type_filter,
        priority_filter=priority_filter,
        limit=limit,
        offset=offset
    )
    
    total = len(notifications)
    unread_count = notification_service.get_unread_count(db=db, user_id=current_user.id)
    
    return {
        "notifications": notifications,
        "total": total,
        "unread_count": unread_count
    }


@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener cantidad de notificaciones no leídas"""
    count = notification_service.get_unread_count(db=db, user_id=current_user.id)
    return {"count": count}


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marcar una notificación como leída"""
    notification = notification_service.mark_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return notification


@router.put("/read-all")
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marcar todas las notificaciones como leídas"""
    updated = notification_service.mark_all_as_read(db=db, user_id=current_user.id)
    return {"message": f"{updated} notifications marked as read"}


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar una notificación"""
    deleted = notification_service.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification deleted successfully"}


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva notificación (admin only)"""
    # TODO: Add admin role check here
    
    try:
        notification_type = NotificationType(notification_data.type)
        notification_priority = NotificationPriority(notification_data.priority)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification type or priority"
        )
    
    notification = notification_service.create_notification(
        db=db,
        user_id=notification_data.user_id,
        type=notification_type,
        priority=notification_priority,
        title=notification_data.title,
        message=notification_data.message,
        link=notification_data.link,
        expires_days=notification_data.expires_days
    )
    
    return notification


# ====== WebSocket Endpoint ======

@router.websocket('/ws')
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    """WebSocket endpoint para notificaciones en tiempo real"""
    try:
        # Validar token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get('sub')
        
        if not user_id_str:
            await websocket.close(code=1008)
            return
        
        user_id = int(user_id_str)
        
        # Conectar usuario
        await manager.connect(user_id, websocket)
        
        try:
            while True:
                # Keep-alive ping/pong
                data = await websocket.receive_text()
                if data == 'ping':
                    await websocket.send_text('pong')
        except WebSocketDisconnect:
            manager.disconnect(user_id, websocket)
    except jwt.PyJWTError:
        try:
            await websocket.close(code=1008)
        except:
            pass
    except Exception as e:
        print(f'WebSocket error: {e}')
        try:
            await websocket.close(code=1011)
        except:
            pass
