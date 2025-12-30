"""
Migration script - excludes GENERATED columns
"""
import pymysql
from datetime import datetime

print("="*80)
print("MIGRATION: licitaciones_adjudicaciones (excluding generated columns)")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

try:
    # Connect
    print("\n[1/7] Connecting...")
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456789',
        port=3306,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("     Connected")
    
    # Get column names from SOURCE (2garantias_seace)
    print("\n[2/7] Getting source column structure...")
    cursor.execute("DESCRIBE `2garantias_seace`.`licitaciones_adjudicaciones`")
    source_columns = [row[0] for row in cursor.fetchall()]
    print(f"     Source has {len(source_columns)} columns")
    
    # Get column names from TARGET that are NOT generated
    print("\n[3/7] Getting target non-generated columns...")
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'garantias_seace'
        AND TABLE_NAME = 'licitaciones_adjudicaciones'
        AND EXTRA NOT LIKE '%GENERATED%'
    """)
    target_safe_columns = [row[0] for row in cursor.fetchall()]
    print(f"     Target has {len(target_safe_columns)} non-generated columns")
    
    # Find common columns
    common_columns = [col for col in source_columns if col in target_safe_columns]
    print(f"     Will copy {len(common_columns)} common columns")
    
    # Count source
    print("\n[4/7] Counting source...")
    cursor.execute("SELECT COUNT(*) FROM `2garantias_seace`.`licitaciones_adjudicaciones`")
    source_total = cursor.fetchone()[0]
    print(f"     Source: {source_total} records")
    
    # Clear target
    print("\n[5/7] Clearing target...")
    cursor.execute("TRUNCATE TABLE `garantias_seace`.`licitaciones_adjudicaciones`")
    conn.commit()
    print("     Cleared")
    
    # Copy data with specific columns
    print("\n[6/7] Copying data...")
    columns_list = ', '.join([f'`{col}`' for col in common_columns])
    sql = f"""
        INSERT INTO `garantias_seace`.`licitaciones_adjudicaciones` 
        ({columns_list})
        SELECT {columns_list}
        FROM `2garantias_seace`.`licitaciones_adjudicaciones`
    """
    cursor.execute(sql)
    conn.commit()
    print(f"     Inserted {cursor.rowcount} records")
    
    # Verify
    print("\n[7/7] Verifying...")
    cursor.execute("SELECT COUNT(*) FROM `garantias_seace`.`licitaciones_adjudicaciones`")
    target_total = cursor.fetchone()[0]
    print(f"     Target: {target_total} records")
    
    # Result
    print("\n[RESULT]")
    if source_total == target_total:
        print(f"     SUCCESS - {target_total} records migrated!")
    else:
        print(f"     PARTIAL - Source:{source_total} Target:{target_total}")
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    if 'conn' in locals():
        conn.close()
    print("\n" + "="*80)
    print("="*80)
