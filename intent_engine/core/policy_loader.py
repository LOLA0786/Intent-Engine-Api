import time
import importlib
import intent_engine.core.policies as policies

_last_reload = 0

def get_policies():
    global _last_reload
    now = time.time()

    if now - _last_reload > 10:  # reload every 10s
        importlib.reload(policies)
        _last_reload = now

    return policies
