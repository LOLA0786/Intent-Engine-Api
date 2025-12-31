from signal_crypto import verify_signal
from signal_schema import canonical_signal_payload

def verify_policy_signals(policy, public_keys):
    """
    policy: list of tuples OR dicts
    public_keys: { provider_name: public_key }
    """
    for item in policy:
        # legacy tuple → nothing to verify
        if isinstance(item, tuple):
            continue

        # signed signal dict
        if isinstance(item, dict):
            if "signature" not in item:
                raise Exception("UNSIGNED_SIGNAL_BLOCKED")

            payload = canonical_signal_payload(item)
            provider = item["provider"]

            if provider not in public_keys:
                raise Exception(f"UNKNOWN_SIGNAL_PROVIDER: {provider}")

            if not verify_signal(public_keys[provider], payload, item["signature"]):
                raise Exception(
                    f"SIGNAL_SIGNATURE_INVALID: {item['signal']}"
                )
