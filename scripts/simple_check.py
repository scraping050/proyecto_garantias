import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456789', port=3306)
cursor = conn.cursor()

# Source
cursor.execute("SELECT COUNT(*) FROM `2garantias_seace`.`licitaciones_adjudicaciones`")
source = cursor.fetchone()[0]

# Target  
cursor.execute("SELECT COUNT(*) FROM `garantias_seace`.`licitaciones_adjudicaciones`")
target = cursor.fetchone()[0]

print(f"Source (2garantias_seace): {source}")
print(f"Target (garantias_seace): {target}")
print(f"Migrated: {target} records")

conn.close()
