def reasoning_agent(state: dict):
    """
    Reasoning Agent:
    - Decides next workflow step based on validation results and issues.
    - Possible decisions:
        - request_missing_info
        - escalate_to_emergency
        - proceed_to_scheduling
        - flag_for_manual_review
    """
    validated = state.get("validated", False)
    issues = state.get("issues", [])

    # Critical symptom detection
    critical_symptoms = [i for i in issues if "Critical symptom detected" in i]

    if critical_symptoms:
        decision = "escalate_to_emergency"
    elif any("Missing info" in i or "Patient name missing" in i for i in issues):
        decision = "request_missing_info"
    elif not validated and issues:
        decision = "flag_for_manual_review"
    else:
        decision = "proceed_to_scheduling"

    print(f"[Reasoning Agent] decision: {decision}")
    return {"decision": decision}
