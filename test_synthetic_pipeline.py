#!/usr/bin/env python3
import sys
from policy_engine import generate_synthetic_data, authorize_intent, infer_risk

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
data = generate_synthetic_data(n)

print(f"\nGenerated {len(data)} synthetics\n")

for i, intent in enumerate(data, 1):
    e = intent["entity"]
    risk = infer_risk(e)
    decision = authorize_intent(intent)

    print(
        f"{i}. {intent['action']:<13} "
        f"${e['amount']:>7,}  "
        f"vel={e['velocity']:.2f}  "
        f"hist={e['history_score']:.2f}  "
        f"→ risk={risk.upper():<6} "
        f"{decision['decision']} ({decision['reason']})"
    )

print("\nPipeline complete.\n")
