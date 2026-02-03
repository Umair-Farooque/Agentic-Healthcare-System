def action_agent(state: dict):
    """
    Action Agent:
    Executes actions based on the Reasoning Agent's decision.
    Updates the 'actions' list in state for audit purposes.
    """
    actions = state.get("actions", [])
    decision = state.get("decision", "")

    if decision == "request_missing_info":
        print("[Action Agent] Requesting missing information from patient...")
        # Simulate sending email/SMS
        actions.append("requested_missing_info")

    elif decision == "escalate_to_emergency":
        print("[Action Agent] Escalating patient to emergency workflow!")
        # Simulate alert to emergency team
        actions.append("escalated_to_emergency")

    elif decision == "proceed_to_scheduling":
        print("[Action Agent] Scheduling patient appointment...")
        # Simulate scheduling
        actions.append("appointment_scheduled")

    elif decision == "flag_for_manual_review":
        print("[Action Agent] Flagging patient for manual review...")
        # Simulate human review
        actions.append("flagged_for_manual_review")

    else:
        print("[Action Agent] Unknown decision, no action taken.")
        actions.append("no_action_taken")

    return {"actions": actions}
