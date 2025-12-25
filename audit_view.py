import json

print("\n=== AUDIT LOG ===\n")

with open("logs/audit.log") as f:
    for line in f:
        e = json.loads(line)
        print(f"Time: {e['timestamp']}")
        print(f"Allowed: {e['allowed']}")
        print(f"Checks: {e['checks']}")
        print(f"Hash: {e['hash']}")
        print("-" * 40)
