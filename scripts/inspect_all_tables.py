import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456789',
    database='garantias_seace',
    port=3306
)

cursor = conn.cursor()

print("="*80)
print("DATABASE STRUCTURE - 4 TABLES")
print("="*80)

tables = ['licitaciones_cabecera', 'licitaciones_adjudicaciones', 'contratos', 'detalle_consorcios']

for table in tables:
    print(f"\n\nTABLE: {table}")
    print("-"*80)
    cursor.execute(f"DESCRIBE {table}")
    for row in cursor.fetchall():
        print(f"  {row[0]:<40} {row[1]:<30} {row[2]}")
    
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"\nTotal rows: {count:,}")
    
    if count > 0:
        cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        sample = cursor.fetchone()
        cols = [desc[0] for desc in cursor.description]
        print(f"\nSample row (first record):")
        for i, col in enumerate(cols):
            val = str(sample[i])[:60] if sample[i] else "NULL"
            print(f"  {col:<40}: {val}")

conn.close()
