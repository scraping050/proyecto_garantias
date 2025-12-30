"""
Fixed script to copy licitaciones_adjudicaciones with proper database name escaping
"""
import pymysql
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'port': 3306,
    'charset': 'utf8mb4'
}

print("="*80)
print("DATA MIGRATION: licitaciones_adjudicaciones")
print(f"Source: `2garantias_seace` -> Target: `garantias_seace`")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

try:
    # Connect to MySQL server (not specific database)
    print("\n1. Connecting to MySQL server...")
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check source table
    print("\n2. Checking source table...")
    cursor.execute("SELECT COUNT(*) FROM `2garantias_seace`.`licitaciones_adjudicaciones`")
    source_count = cursor.fetchone()[0]
    print(f"   Source records: {source_count:,}")
    
    if source_count == 0:
        print("\n⚠️  Source table is empty. Nothing to copy.")
        exit(0)
    
    # Get structure from source
    print("\n3. Analyzing table structure...")
    cursor.execute("DESCRIBE `2garantias_seace`.`licitaciones_adjudicaciones`")
    columns = [row[0] for row in cursor.fetchall()]
    print(f"   Found {len(columns)} columns")
    
    # Clear target table
    print("\n4. Clearing target table...")
    cursor.execute("DELETE FROM `garantias_seace`.`licitaciones_adjudicaciones`")
    conn.commit()
    print("   Target table cleared")
    
    # Copy data in batches
    print("\n5. Copying data...")
    batch_size = 1000
    offset = 0
    total_inserted = 0
    
    while True:
        # Fetch batch from source
        columns_str = ', '.join([f'`{col}`' for col in columns])
        select_query = f"""
            SELECT {columns_str}
            FROM `2garantias_seace`.`licitaciones_adjudicaciones`
            LIMIT {batch_size} OFFSET {offset}
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()
        
        if not rows:
            break
        
        # Insert into target
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"""
            INSERT INTO `garantias_seace`.`licitaciones_adjudicaciones` 
            ({columns_str}) VALUES ({placeholders})
        """
        cursor.executemany(insert_query, rows)
        conn.commit()
        
        total_inserted += len(rows)
        offset += batch_size
        progress = (total_inserted / source_count * 100) if source_count > 0 else 0
        print(f"   Progress: {total_inserted:,}/{source_count:,} ({progress:.1f}%)")
    
    # Verify migration
    print("\n6. Verifying migration...")
    cursor.execute("SELECT COUNT(*) FROM `garantias_seace`.`licitaciones_adjudicaciones`")
    target_count = cursor.fetchone()[0]
    print(f"   Target records: {target_count:,}")
    
    if target_count == source_count:
        print("\n✅ SUCCESS! Migration completed successfully!")
        print(f"   Total records migrated: {target_count:,}")
    else:
        print(f"\n⚠️  WARNING: Record count mismatch!")
        print(f"   Source: {source_count:,}, Target: {target_count:,}")
        print(f"   Difference: {abs(source_count - target_count):,}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    if 'conn' in locals():
        conn.close()
    print("\n" + "="*80)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
