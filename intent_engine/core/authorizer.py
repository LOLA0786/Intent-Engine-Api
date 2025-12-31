import uuid
from intent_engine.config.uaal_config import UAAL_SHADOW_MODE
from intent_engine.core.policies import evaluate_policies
from intent_engine.core.crypto import sign_payload

def authorize(intent):
    evidence_id = str(uuid.uuid4())
    violations = evaluate_policies(intent)

    if violations:
        final = {
            "decision": "BLOCK",
            "violations": violations,
            "evidence_id": evidence_id
        }
    else:
        final = {
            "decision": "ALLOW",
            "evidence_id": evidence_id
        }

    # 🔑 SHADOW MODE NORMALIZATION
    if UAAL_SHADOW_MODE and final["decision"] == "BLOCK":
        payload = {
            "decision": "ALLOW",
            "evidence_id": evidence_id,
            "shadowed": final
        }
    else:
        payload = final

    return sign_payload(payload)
