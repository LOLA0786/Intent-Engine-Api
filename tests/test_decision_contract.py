from intent_engine.core.authorizer import authorize
from intent_engine.core.intent_envelope import build_intent

def test_evidence_id_always_present():
    intent = build_intent(
        "agent_execution",
        {
            "agent_id": "agent-1",
            "tool": "transfer_money",
            "args": {"amount": 999999},
            "environment": "prod",
        },
    )

    signed = authorize(intent)

    # signed envelope must exist
    assert "payload" in signed, "Signed decision missing payload"

    payload = signed["payload"]

    # CRITICAL CONTRACT
    assert "evidence_id" in payload, "evidence_id missing from decision payload"
    assert isinstance(payload["evidence_id"], str)
    assert len(payload["evidence_id"]) > 0
