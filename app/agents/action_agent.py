def action_agent(state: dict):
    print("[Action Agent] performing action...")
    actions = state.get("actions") or []
    actions.append("action_executed")
    return {"actions": actions}
