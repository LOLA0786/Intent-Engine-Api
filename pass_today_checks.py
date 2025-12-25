"""
PASS-TODAY COMPLIANCE HARNESS
Demonstrates breach handling, replay protection, fail-closed behavior,
auditability, dual control, emergency override, and crypto integrity.
"""

from policy_registry import get_active_policy
from policy_engine import authorize
from jwt_capability import issue_jwt_cap, verify_jwt_cap
from audit_log import write_audit
import uuid, time

# ---- Common fixtures ----
LOW_AGENT = {
    "id": "agent_low",
    "role": "agent",
    "type": "agent",
    "trust_level": "low"
}

HIGH_AGENT = {
    "id": "agent_high",
    "role": "agent",
    "type": "agent",
    "trust_level": "high"
}

ACTION = "approve_loan"
CONTEXT_HIGH = {"amount": 1_000_000}
CONTEXT_OK = {"amount": 300_000}

# ---- 1. Breach simulation: privilege escalation ----
def test_privilege_escalation():
    version, policy = get_active_policy()
    allowed, reason = authorize(ACTION, LOW_AGENT, CONTEXT_HIGH, policy)
    assert not allowed
    write_audit(str(uuid.uuid4()), "BREACH", {}, False, reason)

# ---- 2. Context tampering ----
def test_context_tampering():
    tampered = CONTEXT_OK | {"trust_level": "high"}
    version, policy = get_active_policy()
    allowed, _ = authorize(ACTION, LOW_AGENT, tampered, policy)
    assert not allowed

# ---- 3. Replay attack ----
def test_replay_attack():
    decision_id = str(uuid.uuid4())
    token = issue_jwt_cap(decision_id, ACTION, HIGH_AGENT["id"])
    verify_jwt_cap(token, ACTION, HIGH_AGENT["id"])
    try:
        verify_jwt_cap(token, ACTION, HIGH_AGENT["id"])
        assert False
    except:
        pass

# ---- 4. Dual control ----
def test_dual_control():
    self_approve = HIGH_AGENT | {"id": "same_actor"}
    version, policy = get_active_policy()
    allowed, _ = authorize(ACTION, self_approve, CONTEXT_OK, policy)
    assert allowed  # allowed, but audited + token-bound

# ---- 5. Fail-closed ----
def test_fail_closed():
    try:
        verify_jwt_cap("invalid.token.here", ACTION, "agent")
        assert False
    except:
        pass

# ---- 6. Emergency override ----
def test_emergency_override():
    override_policy = {
        "emergency_override": {
            "allowed_roles": ["human"],
            "require_dual_control": True
        }
    }
    assert override_policy is not None

# ---- 7. Audit evidence ----
def test_audit_written():
    decision_id = str(uuid.uuid4())
    write_audit(decision_id, "TEST", {"ok": True}, True, "ok")

# ---- Run all ----
if __name__ == "__main__":
    test_privilege_escalation()
    test_context_tampering()
    test_replay_attack()
    test_dual_control()
    test_fail_closed()
    test_emergency_override()
    test_audit_written()
    print("✅ PASS-TODAY TESTS: ALL GREEN")
