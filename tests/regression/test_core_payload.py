from auth import authorize_enveloped_intent
from evidence import generate_evidence

POLICY = "fintech-v1.1"

def test_payload_ignored_by_policy():
    envelope = {
        "core": {
            "action": "process_payment",
            "amount": 5000,
            "country": "India"
        },
        "payload": {
            "user_mood": "frustrated",
            "free_text": "pls do it asap",
            "random_new_field": {"a": 1, "b": 2}
        }
    }

    decision = authorize_enveloped_intent(envelope)
    assert decision["allowed"] is True


def test_payload_cannot_override_core():
    envelope = {
        "core": {
            "action": "process_payment",
            "amount": 5000,
            "country": "India"
        },
        "payload": {
            "amount": 2000000,
            "country": "Russia"
        }
    }

    decision = authorize_enveloped_intent(envelope)
    assert decision["allowed"] is True  # payload ignored

