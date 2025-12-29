from core.engine import authorize
import threading

print("\n=== CONCURRENCY TEST ===")

def run(i):
    intent = {
        "action": "transfer_funds",
        "amount": 600_000 if i == 7 else 100_000,
        "recipient": f"ENTITY_{i}"
    }
    approvals = {"treasury": True, "compliance": i != 7}
    allowed, audit = authorize(intent, approvals)
    print(f"Agent {i} -> {audit['decision']}")

threads = []
for i in range(10):
    t = threading.Thread(target=run, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
