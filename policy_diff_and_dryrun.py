# Policy Diff + Dry-Run Simulator (fixed)

from copy import deepcopy
from policy_registry import load_policies
from policy_engine import authorize

def policy_diff(version_a: str, version_b: str):
    policies = load_policies()
    pa = policies[version_a]["policy"]
    pb = policies[version_b]["policy"]

    diff = {"added": {}, "removed": {}, "changed": {}}

    for k in pa:
        if k not in pb:
            diff["removed"][k] = pa[k]
        elif pa[k] != pb[k]:
            diff["changed"][k] = {"from": pa[k], "to": pb[k]}

    for k in pb:
        if k not in pa:
            diff["added"][k] = pb[k]

    return diff


def dry_run(version, action, principal, context):
    policies = load_policies()
    policy = deepcopy(policies[version]["policy"])

    allowed, reason = authorize(
        action,
        principal,
        context,
        policy
    )

    return {
        "policy_version": version,
        "action": action,
        "decision": "ALLOW" if allowed else "DENY",
        "reason": reason,
        "dry_run": True
    }
