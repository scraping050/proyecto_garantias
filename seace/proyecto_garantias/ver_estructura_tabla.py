import mysql.connector
import sys
import os

sys.path.insert(0, 'config')
from secrets_manager import get_db_config

def get_table_info(table_name):
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()

        print(f"\nESTRUCTURA DE LA TABLA {table_name}:")
        print("=" * 60)

        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")

        print("\n" + "=" * 60)
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_table_info("Licitaciones_Cabecera")
