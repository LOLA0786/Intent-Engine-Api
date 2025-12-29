import os
import sys

# Ensure repo root is on PYTHONPATH (bulletproof)
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

try:
    from langchain_core.tools import tool
except ImportError:
    # Fallback if LangChain is not installed
    def tool(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.invoke = lambda x: func(**x)
        return wrapper

from integrations.langchain_guardrail import intent_guardrail

@tool
@intent_guardrail
def transfer_money(amount: int):
    """
    Transfer money to a recipient.
    """
    return f"Transferred {amount} successfully"

if __name__ == "__main__":
    print(transfer_money.invoke({"amount": 100}))

    try:
        print(transfer_money.invoke({"amount": 50000}))
    except Exception as e:
        print("Blocked:", e)
