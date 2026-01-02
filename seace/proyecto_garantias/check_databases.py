import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789'
    )
    
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    
    print("\n📊 Bases de datos disponibles:")
    print("=" * 40)
    for (db,) in cursor:
        print(f"  - {db}")
    print("=" * 40)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error: {e}")
