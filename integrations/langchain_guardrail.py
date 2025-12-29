from functools import wraps
from intent_engine_client import (
    authorize_intent,
    IntentDenied,
    IntentEngineUnavailable,
)

def normalize_intent(func_name: str, args: dict) -> dict:
    """
    Convert tool calls into policy-friendly intent.
    This is the critical abstraction boundary.
    """
    intent = {
        "action": func_name,
    }

    # Simple example: flatten common fields
    if "amount" in args:
        intent["amount"] = args["amount"]

    return intent

def intent_guardrail(func):
    """
    One-line pre-execution guardrail for agent tools.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        intent = normalize_intent(func.__name__, kwargs)

        try:
            authorize_intent(intent)
        except IntentEngineUnavailable as e:
            raise RuntimeError(f"CONTROL PLANE DOWN: {e}")
        except IntentDenied as e:
            raise PermissionError(e)

        return func(*args, **kwargs)

    return wrapper
