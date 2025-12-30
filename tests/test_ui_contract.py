import json

with open("ui_contract.json") as f:
    contract = json.load(f)

assert "intent_strength" in contract["visible_to_user"]
assert "risk_flags" in contract["never_visible"]

print("✅ UI contract sanity passed")
