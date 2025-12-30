
from intent_adapters import attach_intent_strength, record_strength_event

    # Intent strength (deterministic)
    if "comparison_intent" in intent:
        intent_strength = attach_intent_strength(
            intent,
            intent["comparison_intent"]
        )
        intent["intent_strength"] = intent_strength
        record_strength_event(intent["intent_id"], intent_strength)
