import json
from intent_engine.core.crypto import sign_payload
from intent_engine.core.merkle import close_day_and_anchor

def sign_daily_root():
    root = close_day_and_anchor()
    return sign_payload(root)
