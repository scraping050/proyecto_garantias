
try:
    with open("full_log.txt", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        found = False
        for i, line in enumerate(lines):
            if "OperationalError" in line or "IntegrityError" in line:
                print(f"--- MATCH AT LINE {i} ---")
                # Truncate line to avoid flooding
                print(line.strip()[:500] + "...")
                for j in range(1, 20):
                    if i+j < len(lines):
                        print(lines[i+j].strip()[:500] + "...")
                found = True
        if not found:
            print("No error found in log.")
            # Print last 20 lines anyway
            print("--- LAST 20 LINES ---")
            for line in lines[-20:]:
                print(line.strip())
except Exception as e:
    print(f"Error reading log: {e}")
