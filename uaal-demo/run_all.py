import bootstrap  # noqa: F401

from tests import (
    test_prompt_injection,
    test_dual_approval,
    test_approval_drift,
    test_hallucination,
    test_concurrency,
    test_reconstruction,
)

print("\n✅ ALL TESTS EXECUTED")
