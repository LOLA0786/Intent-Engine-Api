import json
import hashlib

def canonical_hash(obj: dict) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()

def assert_intent_binding(declared_intent: dict, executed_intent: dict):
    if not declared_intent:
        return  # backward-safe

    if canonical_hash(declared_intent) != canonical_hash(executed_intent):
        raise Exception("INTENT_BINDING_VIOLATION")
