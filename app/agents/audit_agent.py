def audit_agent(state: dict):
    print("[Audit Agent] writing audit log...")
    logs = state.get("audit_log") or []
    logs.append("logged")
    return {"audit_log": logs}
