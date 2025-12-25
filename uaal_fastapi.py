from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from policy_registry import get_active_policy
from policy_engine import authorize
from jwt_capability import issue_jwt_cap, verify_jwt_cap
from audit_log import write_audit
import uuid

app = FastAPI()

class AuthRequest(BaseModel):
    action: str
    principal: dict
    context: dict

@app.post("/authorize")
def authorize_action(req: AuthRequest):
    version, policy = get_active_policy()
    allowed, reason = authorize(
        req.action, req.principal, req.context, policy
    )

    decision_id = str(uuid.uuid4())
    write_audit(decision_id, "AUTHORIZE", req.dict(), allowed, reason)

    if not allowed:
        raise HTTPException(403, reason)

    token = issue_jwt_cap(decision_id, req.action, req.principal["id"])
    return {
        "decision": "ALLOW",
        "decision_id": decision_id,
        "policy_version": version,
        "capability_token": token
    }

@app.post("/execute/{action}")
def execute_action(
    action: str,
    x_capability_token: str = Header(...),
    x_principal_id: str = Header(...)
):
    try:
        payload = verify_jwt_cap(
            x_capability_token, action, x_principal_id
        )
    except Exception as e:
        write_audit("unknown", "EXECUTE", {}, False, str(e))
        raise HTTPException(403, str(e))

    write_audit(
        payload["decision_id"],
        "EXECUTE",
        payload,
        True,
        "Executed"
    )

    return {"status": "EXECUTED", "action": action}
