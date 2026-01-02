import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def check_consortium_schema():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', '123456789'),
            database='garantias_seace'
        )
        cursor = connection.cursor()
        print("\nCOLUMNS IN Detalle_Consorcios:")
        cursor.execute("DESCRIBE Detalle_Consorcios")
        columns = cursor.fetchall()
        for col in columns:
            print(f"- {col[0]} ({col[1]})")
            
        print("\nSample Data (first 5 rows):")
        cursor.execute("SELECT * FROM Detalle_Consorcios LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    check_consortium_schema()
