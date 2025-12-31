import hashlib
import json
from datetime import datetime

def sha256(obj):
    if isinstance(obj, str):
        obj = obj.encode()
    elif isinstance(obj, dict):
        obj = json.dumps(obj, sort_keys=True).encode()
    return hashlib.sha256(obj).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

def build_intent(layer, payload):
    return {
        "layer": layer,
        "payload_hash": sha256(payload),
        "payload": payload,
        "timestamp": now()
    }
