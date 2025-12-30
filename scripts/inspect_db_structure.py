import sys
import os
sys.path.append(os.getcwd())

import pymysql

# Connect to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

print("="*80)
print("DATABASE STRUCTURE INSPECTION")
print("="*80)

try:
    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table_dict in tables:
            table_name = list(table_dict.values())[0]
            
            print(f"\n{'='*80}")
            print(f"TABLE: {table_name}")
            print(f"{'='*80}")
            
            # Get column information
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            print(f"\n{'Field':<30} {'Type':<20} {'Null':<5} {'Key':<5}")
            print("-"*80)
            for col in columns:
                print(f"{col['Field']:<30} {col['Type']:<20} {col['Null']:<5} {col['Key']:<5}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"\nTotal rows: {count:,}")
            
            # Show sample data if table has rows
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                print(f"\nSample data (first row):")
                print("-"*80)
                for key, value in sample.items():
                    value_str = str(value)[:50] if value else "NULL"
                    print(f"{key:<30}: {value_str}")

finally:
    connection.close()

print(f"\n{'='*80}")
print("INSPECTION COMPLETE")
print(f"{'='*80}")
