import os
import sys
import traceback
from sqlalchemy import create_engine, MetaData, Table, text, inspect
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import OperationalError, IntegrityError

# Configuration
SRC_URL = "mysql+pymysql://root:123456789@localhost:3306/garantias_seace3"
DST_URL = "mysql+pymysql://root:123456789@localhost:3306/garantias_seace"

def migrate():
    print(f"Starting migration from {SRC_URL} to {DST_URL}")
    
    # Establish connections
    try:
        src_engine = create_engine(SRC_URL)
        dst_engine = create_engine(DST_URL)
        
        src_conn = src_engine.connect()
        dst_conn = dst_engine.connect()
        
        print("Connected to both databases successfully.")
    except Exception as e:
        print(f"Error connecting to databases: {e}")
        return

    # Reflect metadata
    try:
        src_meta = MetaData()
        src_meta.reflect(bind=src_engine)
        
        dst_meta = MetaData()
        dst_meta.reflect(bind=dst_engine)
        
        # Disable foreign key checks on destination
        dst_conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Try to increase max_allowed_packet to 64MB
        try:
            dst_conn.execute(text("SET GLOBAL max_allowed_packet=67108864"))
            print("  - Set max_allowed_packet to 64MB")
        except Exception as e:
            print(f"  - Warning: Could not set max_allowed_packet: {e}")
        
        # Iterate over source tables
        sorted_tables = src_meta.sorted_tables
        
        for table in sorted_tables:
            table_name = table.name
            print(f"\nProcessing table: {table_name}")
            
            # 1. Create table if it doesn't exist
            if table_name not in dst_meta.tables:
                print(f"  - Table {table_name} does not exist in destination. Creating...")
                table.create(bind=dst_conn)
                print(f"  - Table {table_name} created.")
                dst_table = Table(table_name, dst_meta, autoload_with=dst_conn)
            else:
                print(f"  - Table {table_name} exists.")
                dst_table = dst_meta.tables[table_name]

            # 2. Migrate Data (Upsert)
            print(f"  - Fetching data from source...")
            
            select_stmt = table.select()
            result = src_conn.execute(select_stmt)
            
            rows = [dict(row._mapping) for row in result]
            
            if not rows:
                print("  - No data to migrate.")
                continue
                
            print(f"  - Migrating {len(rows)} rows...")
            
            # Batch insert/upsert
            batch_size = 10 
            
            # Get destination table columns to filter source data
            # Exclude Computed/Generated columns which cannot be inserted into
            dst_columns = set()
            for c in dst_table.columns:
                if not getattr(c, 'computed', None):
                    dst_columns.add(c.name)
                else:
                    print(f"    - Skipping generated column: {c.name}")

            for i in range(0, len(rows), batch_size):
                batch = rows[i:i+batch_size]
                
                # Filter columns for each row
                batch_dicts = []
                for r in batch:
                    # r is a dict already
                    row_dict = {k: v for k, v in r.items() if k in dst_columns}
                    batch_dicts.append(row_dict)
                
                if not batch_dicts:
                    continue
                
                # Prepare Upsert statement
                insert_stmt = insert(dst_table).values(batch_dicts)
                
                # Construct on_duplicate_key_update clauses
                pk_names = [key.name for key in dst_table.primary_key]
                
                update_dict = {}
                # Use the first row to determine columns from the filtered batch
                if batch_dicts:
                    for col in batch_dicts[0].keys():
                        if col not in pk_names:
                             update_dict[col] = insert_stmt.inserted[col]
                
                try:
                    if update_dict:
                        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(update_dict)
                        dst_conn.execute(on_duplicate_key_stmt)
                    else:
                        insert_ignore_stmt = insert_stmt.prefix_with('IGNORE')
                        dst_conn.execute(insert_ignore_stmt)
                except OperationalError as e:
                    # Retry with commit? Or fail
                    raise e
                    
            print(f"  - Batch {i//batch_size + 1} completed.")
            
            # Commit after each table
            dst_conn.commit()
            print(f"  - Data migration for {table_name} completed.")

    except Exception as e:
        print(f"An error occurred during migration: {str(e)[:500]}") # Truncate error message
        if hasattr(e, 'orig'):
            print(f"Original error code: {e.orig}")
        if 'dst_conn' in locals():
            dst_conn.rollback()
    finally:
        if 'dst_conn' in locals():
            try:
                dst_conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
                dst_conn.close()
            except:
                pass
        if 'src_conn' in locals():
            src_conn.close()
        print("\nMigration finished.")

if __name__ == "__main__":
    migrate()
