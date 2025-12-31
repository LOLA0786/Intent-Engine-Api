from intent_engine.adapters.agent_executor import uaal_execute_tool

print(
    uaal_execute_tool(
        agent_id="agent-1",
        tool_name="transfer_money",
        tool_args={"amount": 250000},
        environment="prod"
    )
)
