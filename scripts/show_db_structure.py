"""
Get exact structure of all 4 tables from database
"""
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456789', port=3306, database='garantias_seace')
cursor = conn.cursor()

tables = ['licitaciones_cabecera', 'licitaciones_adjudicaciones', 'contratos', 'detalle_consorcios']

for table in tables:
    print(f"\n{'='*80}")
    print(f"TABLE: {table}")
    print(f"{'='*80}")
    cursor.execute(f"DESCRIBE {table}")
    
    print(f"\n{'Field':<35} {'Type':<25} {'Null':<6} {'Key':<6} {'Extra'}")
    print("-"*80)
    for row in cursor.fetchall():
        print(f"{row[0]:<35} {row[1]:<25} {row[2]:<6} {row[3]:<6} {row[5] if len(row) > 5 else ''}")
    
    # Count records
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"\nTotal records: {count:,}")
    
    # Sample data
    if count > 0:
        cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        sample = cursor.fetchone()
        cols = [desc[0] for desc in cursor.description]
        print(f"\nSample data (first row):")
        for i, col in enumerate(cols):
            val = str(sample[i])[:50] if sample[i] is not None else "NULL"
            print(f"  {col}: {val}")

conn.close()
