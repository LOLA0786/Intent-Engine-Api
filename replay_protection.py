_seen = set()

def check_replay(nonce: str) -> bool:
    if nonce in _seen:
        return False
    _seen.add(nonce)
    return True
