from auth import authorize_intent, shadow_decide_intent

def test_shadow_policy_does_not_block_execution():
    intent = {"action": "process_payment", "amount": 9000, "country": "India"}

    prod = authorize_intent(intent)
    shadow = shadow_decide_intent(intent, "fintech-v2.0")

    # prod still executes
    assert prod["allowed"] is True

    # shadow can disagree safely
    assert shadow["shadow_allowed"] in [True, False]
