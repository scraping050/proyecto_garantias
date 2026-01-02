#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para monitorear el progreso del ETL de Consorcios
"""

import mysql.connector
import sys
import os
from datetime import datetime

# Configuración
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'config'))
from secrets_manager import get_db_config

def monitorear_progreso():
    """Muestra el progreso actual del ETL"""
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor(dictionary=True)
        
        print("=" * 70)
        print("📊 MONITOREO ETL DE CONSORCIOS")
        print("=" * 70)
        print()
        
        # Total procesados
        cursor.execute("SELECT COUNT(*) as total FROM Detalle_Consorcios")
        total_miembros = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT COUNT(DISTINCT id_contrato) as total 
            FROM Detalle_Consorcios
        """)
        contratos_procesados = cursor.fetchone()['total']
        
        # Pendientes
        cursor.execute("""
            SELECT COUNT(*) as pendientes
            FROM Licitaciones_Adjudicaciones a
            LEFT JOIN Detalle_Consorcios d ON a.id_contrato = d.id_contrato
            WHERE a.ganador_nombre LIKE '%CONSORCIO%' 
              AND d.id_contrato IS NULL
              AND a.id_contrato IS NOT NULL AND a.id_contrato != ''
        """)
        pendientes = cursor.fetchone()['pendientes']
        
        # Estadísticas de auditoría
        cursor.execute("""
            SELECT 
                COUNT(*) as total_intentos,
                SUM(CASE WHEN estado = 'EXITO' THEN 1 ELSE 0 END) as exitosos,
                SUM(CASE WHEN estado = 'ERROR' THEN 1 ELSE 0 END) as errores,
                SUM(CASE WHEN estado = 'SALTADO' THEN 1 ELSE 0 END) as saltados,
                SUM(tokens_input) as total_tokens_in,
                SUM(tokens_output) as total_tokens_out,
                SUM(costo_usd) as costo_total,
                MAX(fecha_proceso) as ultimo_proceso
            FROM ETL_Consorcios_Log
        """)
        stats = cursor.fetchone()
        
        print(f"📦 CONTRATOS PROCESADOS:")
        print(f"   Contratos completados: {contratos_procesados:,}")
        print(f"   Miembros extraídos: {total_miembros:,}")
        print(f"   Contratos pendientes: {pendientes:,}")
        print()
        
        if stats and stats['total_intentos'] > 0:
            tasa_exito = (stats['exitosos'] / stats['total_intentos'] * 100) if stats['total_intentos'] > 0 else 0
            
            print(f"📈 ESTADÍSTICAS DE PROCESAMIENTO:")
            print(f"   Total intentos: {stats['total_intentos']:,}")
            print(f"   Exitosos: {stats['exitosos']:,} ({tasa_exito:.1f}%)")
            print(f"   Errores: {stats['errores']:,}")
            print(f"   Saltados: {stats['saltados']:,}")
            print()
            
            print(f"💰 CONSUMO DE API:")
            print(f"   Tokens input: {stats['total_tokens_in']:,}")
            print(f"   Tokens output: {stats['total_tokens_out']:,}")
            print(f"   Costo total: ${stats['costo_total']:.4f} USD")
            print()
            
            if stats['ultimo_proceso']:
                print(f"⏱️  Último procesamiento: {stats['ultimo_proceso']}")
            print()
        
        # Progreso
        total_inicial = 2084
        progreso = ((total_inicial - pendientes) / total_inicial * 100) if total_inicial > 0 else 0
        
        print(f"📊 PROGRESO GENERAL:")
        print(f"   Completado: {progreso:.1f}%")
        print(f"   [{('█' * int(progreso/2))}{('░' * (50-int(progreso/2)))}]")
        print()
        
        # Estimación de tiempo restante
        if stats and stats['exitosos'] > 0 and pendientes > 0:
            tiempo_promedio = 30  # segundos por contrato (estimación)
            tiempo_restante_seg = pendientes * tiempo_promedio
            horas_restantes = tiempo_restante_seg / 3600
            
            print(f"⏳ TIEMPO ESTIMADO RESTANTE:")
            print(f"   {horas_restantes:.1f} horas (~{horas_restantes/24:.1f} días)")
        
        print()
        print("=" * 70)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    monitorear_progreso()
