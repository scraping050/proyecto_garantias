import pymysql
import sys

# Configuration for the SOURCE database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "2garantias_seace",
    "port": 3306,
    "cursorclass": pymysql.cursors.DictCursor
}

def inspect_db():
    output_file = "inspection_result.txt"
    print(f"Connecting to {DB_CONFIG['database']}...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
    except Exception as e:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Error connecting to database: {e}")
        return

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            with connection.cursor() as cursor:
                # Get list of tables
                cursor.execute("SHOW TABLES")
                tables = [list(row.values())[0] for row in cursor.fetchall()]
                
                if not tables:
                    f.write("No tables found in the database.\n")
                    return

                f.write(f"Found {len(tables)} tables: {', '.join(tables)}\n")

                for table in tables:
                    f.write(f"\nTABLE: {table}\n")
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) as count FROM `{table}`")
                    count = cursor.fetchone()['count']
                    f.write(f"Total Rows: {count}\n")

                    # Get schema
                    cursor.execute(f"DESCRIBE `{table}`")
                    schema = cursor.fetchall()
                    
                    f.write("COLUMNS:\n")
                    for col in schema:
                        f.write(f"  - {col['Field']} ({col['Type']})\n")
        
        print(f"Inspection complete. Results written to {output_file}")

    finally:
        connection.close()

if __name__ == "__main__":
    inspect_db()
