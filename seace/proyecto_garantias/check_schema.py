import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def check_schema():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', '123456789'),
            database='garantias_seace'
        )
        cursor = connection.cursor()
        cursor.execute("DESCRIBE licitaciones_cabecera")
        columns = cursor.fetchall()
        print("COLUMNS IN licitaciones_cabecera:")
        for col in columns:
            print(f"- {col[0]} ({col[1]})")
            
        print("\nCOLUMNS IN licitaciones_adjudicaciones:")
        cursor.execute("DESCRIBE licitaciones_adjudicaciones")
        columns_adj = cursor.fetchall()
        for col in columns_adj:
            print(f"- {col[0]} ({col[1]})")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    check_schema()
