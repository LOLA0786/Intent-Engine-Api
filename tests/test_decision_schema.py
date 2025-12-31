from intent_engine.core.authorizer import authorize
from intent_engine.core.intent_envelope import build_intent
from intent_engine.contracts.decision_schema import SignedDecision

def test_signed_decision_schema_valid():
    intent = build_intent(
        "agent_execution",
        {
            "agent_id": "agent-1",
            "tool": "noop",
            "args": {},
            "environment": "prod",
        },
    )

    signed = authorize(intent)
    SignedDecision(**signed)  # should not raise
