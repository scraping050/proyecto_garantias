import os
import sys
from sqlalchemy import text

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine

def import_data():
    dump_file = "dump.sql"
    if not os.path.exists(dump_file):
        print(f"Error: {dump_file} not found. Please save your SQL dump to this file in the root directory.")
        return

    print("Reading SQL dump...")
    try:
        with open(dump_file, "r", encoding="utf-8") as f:
            sql_content = f.read()
    except UnicodeDecodeError:
        try:
            with open(dump_file, "r", encoding="latin-1") as f:
                sql_content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return

    # Split by semicolon to get individual statements
    # Note: This is a simple splitter and might break if data contains semicolons.
    # For the provided dump (INSERTs), it should be fine.
    statements = sql_content.split(';')
    
    print(f"Found {len(statements)} statements to execute.")

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # Disable foreign key checks for bulk operations
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            
            for i, statement in enumerate(statements):
                stmt = statement.strip()
                if not stmt:
                    continue
                
                # Skip comments
                if stmt.startswith("--") or stmt.startswith("/*"):
                    continue
                    
                # Skip database creation/selection to use the configured DB
                if stmt.upper().startswith("CREATE DATABASE") or stmt.upper().startswith("USE"):
                    print(f"Skipping DB command: {stmt[:50]}...")
                    continue

                try:
                    # Execute statement
                    connection.execute(text(stmt))
                    if i % 10 == 0:
                        print(f"Executed statement {i+1}...")
                except Exception as e:
                    print(f"Error executing statement {i+1}: {stmt[:100]}... \nError: {e}")
                    # Decide whether to stop or continue. For now, we continue.
            
            # Re-enable foreign key checks
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            
            trans.commit()
            print("Import completed successfully.")
        except Exception as e:
            trans.rollback()
            print(f"Import failed: {e}")

if __name__ == "__main__":
    import_data()
