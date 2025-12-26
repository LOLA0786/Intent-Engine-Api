import json
import hashlib
from typing import Dict, Any, List
import os

_AUDIT_CHAIN_FILE = "audit_chain.json"  # Local only; gitignore'd

def hash_entry(entry: Dict[str, Any]) -> str:
    entry_str = json.dumps(entry, sort_keys=True)
    return hashlib.sha256(entry_str.encode()).hexdigest()

def append_to_chain(intent: Dict[str, Any], decision: Dict[str, Any], exec_result: Any = None) -> str:
    entry = {
        "timestamp": intent.get("timestamp"),
        "intent": intent,
        "decision": decision,
        "execution": exec_result,
        "entry_hash": None,  # Self-hash
        "prev_hash": get_latest_hash()
    }
    entry["entry_hash"] = hash_entry(entry)
    chain = load_chain()
    chain.append(entry)
    save_chain(chain)
    return entry["entry_hash"]

def get_latest_hash() -> str:
    chain = load_chain()
    return chain[-1]["entry_hash"] if chain else "genesis"

def load_chain() -> List[Dict]:
    if os.path.exists(_AUDIT_CHAIN_FILE):
        with open(_AUDIT_CHAIN_FILE, 'r') as f:
            return json.load(f)
    return []

def save_chain(chain: List[Dict]):
    with open(_AUDIT_CHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=2)

def get_audit_chain(limit: int = 100) -> List[Dict]:
    return load_chain()[-limit:]
