"""
WebSocket Connection Manager - Gestiona conexiones WebSocket para notificaciones en tiempo real
"""
from fastapi import WebSocket
from typing import Dict, List
import logging
import json

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Gestor de conexiones WebSocket por usuario"""
    
    def __init__(self):
        # Diccionario: user_id -> List[WebSocket]
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket):
        """Conectar un WebSocket para un usuario"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        logger.info(f"✅ WebSocket conectado para user_id={user_id}. Total conexiones: {self.get_connection_count(user_id)}")
    
    def disconnect(self, user_id: int, websocket: WebSocket):
        """Desconectar un WebSocket"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
                logger.info(f"❌ WebSocket desconectado para user_id={user_id}")
            
            # Limpiar si no quedan conexiones
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_notification(self, user_id: int, notification: dict):
        """Enviar notificación a un usuario específico"""
        if user_id not in self.active_connections:
            logger.debug(f"User {user_id} no tiene conexiones activas")
            return
        
        # Enviar a todas las conexiones del usuario (múltiples tabs/dispositivos)
        disconnected = []
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(notification)
            except Exception as e:
                logger.error(f"Error enviando a user_id={user_id}: {e}")
                disconnected.append(connection)
        
        # Limpiar conexiones muertas
        for conn in disconnected:
            self.disconnect(user_id, conn)
    
    async def broadcast_to_all(self, notification: dict):
        """Broadcast a todos los usuarios conectados"""
        for user_id in list(self.active_connections.keys()):
            await self.send_personal_notification(user_id, notification)
    
    def get_connection_count(self, user_id: int) -> int:
        """Obtener cantidad de conexiones para un usuario"""
        return len(self.active_connections.get(user_id, []))
    
    def get_total_connections(self) -> int:
        """Obtener cantidad total de conexiones activas"""
        return sum(len(conns) for conns in self.active_connections.values())
    
    def get_connected_users(self) -> List[int]:
        """Obtener lista de user_ids conectados"""
        return list(self.active_connections.keys())


# Singleton global
manager = ConnectionManager()
