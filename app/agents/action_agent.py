def action_agent(state: dict):
    """
    Action Agent:
    Executes the decision made by Reasoning Agent.
    Simulated actions for now.
    """

    actions = state.get("actions") or []
    decision = state.get("decision", "")

    if decision == "request_missing_info":
        print("[Action Agent] Requesting missing information from patient...")
        actions.append("requested_missing_info")
    elif decision == "proceed_to_scheduling":
        print("[Action Agent] Proceeding to patient scheduling...")
        actions.append("scheduled_patient")
    elif decision == "flag_for_manual_review":
        print("[Action Agent] Flagging for manual review...")
        actions.append("flagged_manual_review")
    else:
        print("[Action Agent] Unknown decision, logging action...")
        actions.append(f"executed_unknown_decision:{decision}")

    return {"actions": actions}
