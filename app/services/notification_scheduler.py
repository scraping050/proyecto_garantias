"""
Notification Scheduler - Programa ejecución automática de triggers
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from app.database import SessionLocal
from app.services.notification_triggers import notification_triggers
import logging

logger = logging.getLogger(__name__)

# Crear scheduler global
scheduler = BackgroundScheduler()


def run_carta_fianza_check():
    """Job para verificar cartas fianza"""
    db = SessionLocal()
    try:
        count = notification_triggers.check_carta_fianza_expiration(db)
        logger.info(f"[Scheduler] Cartas Fianza check: {count} notificaciones")
    except Exception as e:
        logger.error(f"[Scheduler] Error en carta_fianza_check: {e}")
    finally:
        db.close()


def run_licitaciones_check():
    """Job para verificar nuevas licitaciones"""
    db = SessionLocal()
    try:
        count = notification_triggers.check_new_licitaciones(db)
        logger.info(f"[Scheduler] Licitaciones check: {count} notificaciones")
    except Exception as e:
        logger.error(f"[Scheduler] Error en licitaciones_check: {e}")
    finally:
        db.close()


def run_adjudicaciones_check():
    """Job para verificar adjudicaciones"""
    db = SessionLocal()
    try:
        count = notification_triggers.check_new_adjudicaciones(db)
        logger.info(f"[Scheduler] Adjudicaciones check: {count} notificaciones")
    except Exception as e:
        logger.error(f"[Scheduler] Error en adjudicaciones_check: {e}")
    finally:
        db.close()


def run_changes_check():
    """Job para verificar cambios importantes"""
    db = SessionLocal()
    try:
        count = notification_triggers.check_important_changes(db)
        logger.info(f"[Scheduler] Changes check: {count} notificaciones")
    except Exception as e:
        logger.error(f"[Scheduler] Error en changes_check: {e}")
    finally:
        db.close()


def start_scheduler():
    """Iniciar el scheduler con todos los jobs"""
    
    if scheduler.running:
        logger.warning("Scheduler ya está en ejecución")
        return
    
    # Job 1: Cartas Fianza - Diariamente a las 8:00 AM
    scheduler.add_job(
        run_carta_fianza_check,
        trigger=CronTrigger(hour=8, minute=0),
        id='carta_fianza_daily',
        name='Check Carta Fianza Expiration',
        replace_existing=True
    )
    
    # Job 2: Nuevas Licitaciones - Cada hora
    scheduler.add_job(
        run_licitaciones_check,
        trigger=IntervalTrigger(hours=1),
        id='licitaciones_hourly',
        name='Check New Licitaciones',
        replace_existing=True
    )
    
    # Job 3: Adjudicaciones - Cada 30 minutos
    scheduler.add_job(
        run_adjudicaciones_check,
        trigger=IntervalTrigger(minutes=30),
        id='adjudicaciones_half_hourly',
        name='Check New Adjudicaciones',
        replace_existing=True
    )
    
    # Job 4: Cambios importantes - Cada hora
    scheduler.add_job(
        run_changes_check,
        trigger=IntervalTrigger(hours=1),
        id='changes_hourly',
        name='Check Important Changes',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("✅ Notification Scheduler iniciado con 4 jobs")
    logger.info("  - Cartas Fianza: Diariamente 8:00 AM")
    logger.info("  - Licitaciones: Cada hora")
    logger.info("  - Adjudicaciones: Cada 30 minutos")
    logger.info("  - Cambios: Cada hora")


def stop_scheduler():
    """Detener el scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler detenido")
