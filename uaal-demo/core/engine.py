from core.policy import evaluate_policy
from core.audit import log_decision
from core.intent import canonical_hash

def authorize(executed_intent, approvals=None, declared_intent=None):
    # 🔐 Intent binding check
    if declared_intent:
        if canonical_hash(declared_intent) != canonical_hash(executed_intent):
            audit = log_decision(
                executed_intent,
                False,
                "Declared intent does not match executed intent (possible prompt injection)"
            )
            return False, audit

    allowed, reason = evaluate_policy(executed_intent, approvals)
    audit = log_decision(executed_intent, allowed, reason)
    return allowed, audit
