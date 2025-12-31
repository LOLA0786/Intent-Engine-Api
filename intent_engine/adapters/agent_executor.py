from intent_engine.core.intent_envelope import build_intent
from intent_engine.core.authorizer import authorize

def uaal_execute_tool(agent_id, tool_name, tool_args, environment="prod"):
    intent = build_intent("agent_execution", {
        "agent_id": agent_id,
        "tool": tool_name,
        "args": tool_args,
        "environment": environment
    })

    signed = authorize(intent)

    # 🔑 unwrap signed decision
    decision = signed["payload"]

    if decision["decision"] == "BLOCK":
        return {
            "status": "blocked",
            "evidence_id": decision["evidence_id"]
        }

    if decision["decision"] == "REQUIRE_HUMAN":
        return {
            "status": "paused",
            "reason": "human_approval_required",
            "evidence_id": decision["evidence_id"]
        }

    return {
        "status": "executed",
        "tool": tool_name,
        "args": tool_args,
        "evidence_id": decision["evidence_id"]
    }
