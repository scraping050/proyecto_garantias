-- Script SQL para insertar notificaciones de prueba
-- Ejecutar en MySQL después de crear la tabla notifications

-- Primero, obtener el ID de un usuario existente (ajustar según tu base de datos)
SET @user_id = (SELECT id FROM usuarios LIMIT 1);

-- Insertar notificaciones de prueba
INSERT INTO notifications (
    user_id, type, priority, title, message, link, is_read, created_at, expires_at
) VALUES
    -- Notificación 1: Alta prioridad - Licitación
    (@user_id, 'licitacion', 'high', 'Nueva Licitación Publicada', 'Se ha publicado una nueva licitación en la categoría OBRAS por un monto de S/ 2,350,000', '/seace/busqueda', FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
    
    -- Notificación 2: Media prioridad - Carta Fianza
    (@user_id, 'carta_fianza', 'medium', 'Carta Fianza próxima a vencer', 'La carta fianza #CF-2024-001 vencerá en 15 días', '/mqs/fianzas', FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
    
    -- Notificación 3: Alta prioridad - Adjudicación
    (@user_id, 'adjudicacion', 'high', 'Adjudicación Confirmada', 'Se ha confirmado la adjudicación de la licitación ADJ-2024-0045', '/seace/licitaciones/12345', FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
    
    -- Notificación 4: Baja prioridad - Reporte
    (@user_id, 'reporte', 'low', 'Reporte Mensual Generado', 'El reporte de garantías del mes de Diciembre está disponible', '/seace/reportes', FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
    
    -- Notificación 5: Media prioridad - Sistema
    (@user_id, 'sistema', 'medium', 'Actualización del Sistema', 'El sistema se actualizó a la versión 3.0.0 con nuevas funcionalidades', NULL, FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
    
    -- Notificación 6: Baja prioridad - Consorcio
    (@user_id, 'consorcio', 'low', 'Nuevo Consorcio Registrado', 'Se ha registrado un nuevo consorcio: Constructora Unidos SAC', '/mqs/obras', FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY)),
    
    -- Notificación 7: Media prioridad - Licitación
    (@user_id, 'licitacion', 'medium', 'Licitación en Estado ADJUDICADO', 'La licitación LIC-2024-0234 cambió a estado ADJUDICADO', '/seace/busqueda', FALSE, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY));

-- Verificar notificaciones creadas
SELECT COUNT(*) as total_notifications FROM notifications WHERE user_id = @user_id;
SELECT COUNT(*) as unread_notifications FROM notifications WHERE user_id = @user_id AND is_read = FALSE;
