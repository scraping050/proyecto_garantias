"""
Simple and clean migration script - NO unicode characters
"""
import pymysql
from datetime import datetime

print("="*80)
print("MIGRATION: licitaciones_adjudicaciones")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

try:
    # Connect
    print("\n[1/6] Connecting to database...")
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456789',
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("     Connected OK")
    
    # Check source
    print("\n[2/6] Counting source records...")
    cursor.execute("SELECT COUNT(*) FROM `2garantias_seace`.`licitaciones_adjudicaciones`")
    source_total = cursor.fetchone()[0]
    print(f"     Source has {source_total} records")
    
    if source_total == 0:
        print("\n[!] Source is empty - nothing to copy")
        exit(0)
    
    # Clear target
    print("\n[3/6] Clearing target table...")
    cursor.execute("TRUNCATE TABLE `garantias_seace`.`licitaciones_adjudicaciones`")
    conn.commit()
    print("     Target cleared")
    
    # Copy data using INSERT SELECT
    print("\n[4/6] Copying data...")
    cursor.execute("""
        INSERT INTO `garantias_seace`.`licitaciones_adjudicaciones`
        SELECT * FROM `2garantias_seace`.`licitaciones_adjudicaciones`
    """)
    conn.commit()
    print(f"     Copied {cursor.rowcount} records")
    
    # Verify
    print("\n[5/6] Verifying...")
    cursor.execute("SELECT COUNT(*) FROM `garantias_seace`.`licitaciones_adjudicaciones`")
    target_total = cursor.fetchone()[0]
    print(f"     Target now has {target_total} records")
    
    # Result
    print("\n[6/6] Result:")
    if source_total == target_total:
        print(f"     SUCCESS - {target_total} records migrated")
    else:
        print(f"     MISMATCH - Source:{source_total} Target:{target_total}")
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    if 'conn' in locals():
        conn.close()
    print("\n" + "="*80)
    print("DONE")
    print("="*80)
