#!/usr/bin/env python3
from policy_engine import generate_synthetic_data, authorize_intent
import sys

num_tests = int(sys.argv[1]) if len(sys.argv) > 1 else 3
synthetics = generate_synthetic_data(num_tests)

for intent in synthetics:
    decision = authorize_intent(intent)
    print(f"{intent['action']} {intent['entity']['amount']} {intent['entity']['risk']} → {decision['decision']} {decision['reason']}")

print("\nPipeline complete. For full Redis/Fabric: Run via API /test-batch.")
