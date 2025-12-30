"""
Quick verification of migration results
"""
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456789',
    port=3306
)

cursor = conn.cursor()

# Check source
cursor.execute("SELECT COUNT(*) FROM `2garantias_seace`.`licitaciones_adjudicaciones`")
source_count = cursor.fetchone()[0]

# Check target
cursor.execute("SELECT COUNT(*) FROM `garantias_seace`.`licitaciones_adjudicaciones`")
target_count = cursor.fetchone()[0]

# Check sample data
cursor.execute("SELECT * FROM `garantias_seace`.`licitaciones_adjudicaciones` LIMIT 1")
sample = cursor.fetchone()

print("="*60)
print("MIGRATION VERIFICATION")
print("="*60)
print(f"Source (2garantias_seace): {source_count:,} records")
print(f"Target (garantias_seace):  {target_count:,} records")
print(f"Match: {'✅ YES' if source_count == target_count else '❌ NO'}")
print(f"Sample record exists: {'✅ YES' if sample else '❌ NO'}")
print("="*60)

conn.close()
