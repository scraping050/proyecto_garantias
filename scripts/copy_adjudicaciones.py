"""
Script to copy licitaciones_adjudicaciones data from 2garantias_seace to garantias_seace
"""
import pymysql
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

print("="*80)
print("MIGRATION: licitaciones_adjudicaciones")
print(f"Source: 2garantias_seace -> Target: garantias_seace")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

try:
    # Connect to source database
    print("\n1. Connecting to source database (2garantias_seace)...")
    source_conn = pymysql.connect(**DB_CONFIG, database='2garantias_seace')
    source_cursor = source_conn.cursor()
    
    # Connect to target database
    print("2. Connecting to target database (garantias_seace)...")
    target_conn = pymysql.connect(**DB_CONFIG, database='garantias_seace')
    target_cursor = target_conn.cursor()
    
    # Get count from source
    print("\n3. Checking source data...")
    source_cursor.execute("SELECT COUNT(*) as total FROM licitaciones_adjudicaciones")
    source_count = source_cursor.fetchone()['total']
    print(f"   Source records: {source_count:,}")
    
    if source_count == 0:
        print("\n⚠️  Source table is empty. Nothing to copy.")
    else:
        # Clear target table first
        print("\n4. Clearing target table...")
        target_cursor.execute("DELETE FROM licitaciones_adjudicaciones")
        target_conn.commit()
        print("   Target table cleared.")
        
        # Fetch all data from source
        print("\n5. Fetching data from source...")
        source_cursor.execute("SELECT * FROM licitaciones_adjudicaciones")
        records = source_cursor.fetchall()
        print(f"   Fetched {len(records):,} records")
        
        # Get column names
        columns = list(records[0].keys()) if records else []
        
        # Insert into target in batches
        print("\n6. Inserting into target...")
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            
            # Build INSERT query
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join([f"`{col}`" for col in columns])
            insert_query = f"INSERT INTO licitaciones_adjudicaciones ({columns_str}) VALUES ({placeholders})"
            
            # Prepare values
            values = []
            for record in batch:
                values.append(tuple(record[col] for col in columns))
            
            # Execute batch insert
            target_cursor.executemany(insert_query, values)
            target_conn.commit()
            
            total_inserted += len(batch)
            print(f"   Progress: {total_inserted:,}/{len(records):,} records ({(total_inserted/len(records)*100):.1f}%)")
        
        # Verify target count
        print("\n7. Verifying migration...")
        target_cursor.execute("SELECT COUNT(*) as total FROM licitaciones_adjudicaciones")
        target_count = target_cursor.fetchone()['total']
        print(f"   Target records: {target_count:,}")
        
        if target_count == source_count:
            print("\n✅ Migration completed successfully!")
            print(f"   Total records migrated: {target_count:,}")
        else:
            print(f"\n⚠️  Warning: Record count mismatch!")
            print(f"   Source: {source_count:,}, Target: {target_count:,}")
    
except Exception as e:
    print(f"\n❌ Error during migration: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Close connections
    if 'source_conn' in locals():
        source_conn.close()
    if 'target_conn' in locals():
        target_conn.close()
    print("\n" + "="*80)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
