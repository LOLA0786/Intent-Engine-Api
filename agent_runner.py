import requests
import json
import subprocess
import sys

UAAL_URL = "http://127.0.0.1:9000/test"

# ---- STEP A: LLM TOOL CALL (SAFE INTENT) ----
tool_call = {
    "tool_name": "transfer_funds",
    "arguments": {
        "from_account": "ACC-001",
        "to_account": "ACC-002",
        "amount": 50000,
        "currency": "INR",
        "new_beneficiary": False
    }
}

print("\n🧠 LLM TOOL CALL:")
print(json.dumps(tool_call, indent=2))

# ---- STEP B: Normalize → UAAL intent ----
uaal_payload = {
    "framework": "openai-function-call",
    "input": {
        "domain": "fintech",
        "action": "transfer_funds",
        "amount": tool_call["arguments"]["amount"],
        "new_beneficiary": tool_call["arguments"]["new_beneficiary"]
    }
}

# ---- STEP C: UAAL CHECK (ENFORCE MODE) ----
resp = requests.post(
    UAAL_URL,
    headers={
        "Content-Type": "application/json",
        "X-UAAL-Mode": "enforce"
    },
    json=uaal_payload
)

decision = resp.json()

print("\n🛡 UAAL DECISION:")
print(json.dumps(decision, indent=2))

# ---- STEP D: EXECUTION GATE ----
if decision.get("allowed"):
    print("\n✅ EXECUTION ALLOWED")
    subprocess.run(["python3", "mock_tool.py", json.dumps(tool_call["arguments"])])
else:
    print("\n⛔ EXECUTION BLOCKED — TOOL NOT RUN")
    sys.exit(0)
