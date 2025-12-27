import json

def summarize(path="logs/routing.log"):
    total = 0
    cost = 0
    latency = 0
    failures = 0

    with open(path) as f:
        for line in f:
            e = json.loads(line)
            if "outcome" not in e:
                continue

            total += 1
            cost += e["outcome"]["cost"]
            latency += e["outcome"]["latency_ms"]
            if not e["outcome"]["success"]:
                failures += 1

    return {
        "requests": total,
        "avg_cost": cost / total if total else 0,
        "avg_latency_ms": latency / total if total else 0,
        "failure_rate": failures / total if total else 0
    }

# --------------------------------------------------
# Public adapter for audit / kill-tests
# --------------------------------------------------
def calculate_exposure(rows):
    """
    Calculate total exposure from audit decisions.
    Expects rows with: amount, risk_score.
    """
    total = 0.0
    for r in rows:
        try:
            total += float(r.get("amount", 0)) * float(r.get("risk_score", 0))
        except Exception:
            continue
    return total
