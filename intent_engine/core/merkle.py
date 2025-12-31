import hashlib

_last_hash = None

def hash_entry(entry: str):
    return hashlib.sha256(entry.encode()).hexdigest()

def merkle_append(entry: str):
    global _last_hash
    combined = entry if not _last_hash else _last_hash + entry
    _last_hash = hash_entry(combined)
    return _last_hash

def current_root():
    return _last_hash
