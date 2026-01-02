#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar todos los estados presentes en la base de datos
"""

import mysql.connector
from collections import Counter
import json

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'garantias_seace'
}

def analizar_estados():
    """Analiza todos los estados en la base de datos"""
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("=" * 80)
        print("ANÁLISIS DE ESTADOS EN LA BASE DE DATOS")
        print("=" * 80)
        print()
        
        # 1. Estados del proceso (estado_proceso)
        print("1. ESTADOS DEL PROCESO (estado_proceso)")
        print("-" * 80)
        cursor.execute("""
            SELECT estado_proceso, COUNT(*) as cantidad
            FROM Licitaciones_Cabecera
            WHERE estado_proceso IS NOT NULL
            GROUP BY estado_proceso
            ORDER BY cantidad DESC
        """)
        estados_proceso = cursor.fetchall()
        
        total_proceso = sum(e['cantidad'] for e in estados_proceso)
        print(f"Total de registros con estado_proceso: {total_proceso:,}")
        print()
        
        for estado in estados_proceso:
            porcentaje = (estado['cantidad'] / total_proceso * 100) if total_proceso > 0 else 0
            print(f"  {estado['estado_proceso']:<40} {estado['cantidad']:>8,} ({porcentaje:>6.2f}%)")
        
        print()
        print()
        
        # 2. Estados del ítem (estado_item)
        print("2. ESTADOS DEL ÍTEM (estado_item)")
        print("-" * 80)
        cursor.execute("""
            SELECT estado_item, COUNT(*) as cantidad
            FROM Licitaciones_Cabecera
            WHERE estado_item IS NOT NULL
            GROUP BY estado_item
            ORDER BY cantidad DESC
        """)
        estados_item = cursor.fetchall()
        
        total_item = sum(e['cantidad'] for e in estados_item)
        print(f"Total de registros con estado_item: {total_item:,}")
        print()
        
        for estado in estados_item:
            porcentaje = (estado['cantidad'] / total_item * 100) if total_item > 0 else 0
            print(f"  {estado['estado_item']:<40} {estado['cantidad']:>8,} ({porcentaje:>6.2f}%)")
        
        print()
        print()
        
        # 3. Combinaciones de estados
        print("3. COMBINACIONES ESTADO_PROCESO + ESTADO_ITEM (Top 20)")
        print("-" * 80)
        cursor.execute("""
            SELECT 
                estado_proceso,
                estado_item,
                COUNT(*) as cantidad
            FROM Licitaciones_Cabecera
            GROUP BY estado_proceso, estado_item
            ORDER BY cantidad DESC
            LIMIT 20
        """)
        combinaciones = cursor.fetchall()
        
        print(f"{'Estado Proceso':<30} {'Estado Ítem':<30} {'Cantidad':>10}")
        print("-" * 80)
        for combo in combinaciones:
            ep = combo['estado_proceso'] or 'NULL'
            ei = combo['estado_item'] or 'NULL'
            print(f"{ep:<30} {ei:<30} {combo['cantidad']:>10,}")
        
        print()
        print()
        
        # 4. Registros con estados NULL
        print("4. REGISTROS CON ESTADOS NULL")
        print("-" * 80)
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN estado_proceso IS NULL THEN 1 ELSE 0 END) as proceso_null,
                SUM(CASE WHEN estado_item IS NULL THEN 1 ELSE 0 END) as item_null,
                SUM(CASE WHEN estado_proceso IS NULL AND estado_item IS NULL THEN 1 ELSE 0 END) as ambos_null
            FROM Licitaciones_Cabecera
        """)
        nulls = cursor.fetchone()
        
        print(f"Total de registros: {nulls['total']:,}")
        print(f"  - Con estado_proceso NULL: {nulls['proceso_null']:,}")
        print(f"  - Con estado_item NULL: {nulls['item_null']:,}")
        print(f"  - Con ambos NULL: {nulls['ambos_null']:,}")
        
        print()
        print()
        
        # 5. Resumen JSON
        print("5. RESUMEN EN FORMATO JSON")
        print("-" * 80)
        
        resumen = {
            'estados_proceso': {e['estado_proceso']: e['cantidad'] for e in estados_proceso},
            'estados_item': {e['estado_item']: e['cantidad'] for e in estados_item},
            'total_registros': nulls['total'],
            'registros_null': {
                'proceso': nulls['proceso_null'],
                'item': nulls['item_null'],
                'ambos': nulls['ambos_null']
            }
        }
        
        print(json.dumps(resumen, indent=2, ensure_ascii=False))
        
        print()
        print("=" * 80)
        print("ANÁLISIS COMPLETADO")
        print("=" * 80)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error de base de datos: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analizar_estados()
