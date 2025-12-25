# UAAL API Middleware: Policy → Capability → Execution

from flask import Flask, request, jsonify
from policy_registry import get_active_policy
from policy_engine import authorize
from capability_token import consume_capability, issue_capability
import uuid

app = Flask(__name__)

# ---- STEP 1: AUTHORIZE + ISSUE CAPABILITY ----
@app.route("/authorize", methods=["POST"])
def authorize_action():
    data = request.json
    principal = data["principal"]
    action = data["action"]
    context = data["context"]

    version, policy = get_active_policy()
    allowed, reason = authorize(action, principal, context, policy)

    if not allowed:
        return jsonify({
            "decision": "DENY",
            "reason": reason,
            "policy_version": version
        }), 403

    decision_id = str(uuid.uuid4())
    cap_id = issue_capability(decision_id, action, principal["id"])

    return jsonify({
        "decision": "ALLOW",
        "policy_version": version,
        "decision_id": decision_id,
        "capability_token": cap_id
    })


# ---- STEP 2: EXECUTE API USING CAPABILITY ----
@app.route("/execute/<action>", methods=["POST"])
def execute_action(action):
    cap_id = request.headers.get("X-Capability-Token")
    principal_id = request.headers.get("X-Principal-ID")

    ok, msg = consume_capability(cap_id, action, principal_id)
    if not ok:
        return jsonify({"error": msg}), 403

    # 🔥 REAL BUSINESS LOGIC GOES HERE
    return jsonify({
        "status": "EXECUTED",
        "action": action,
        "principal": principal_id
    })


if __name__ == "__main__":
    app.run(port=8000)
