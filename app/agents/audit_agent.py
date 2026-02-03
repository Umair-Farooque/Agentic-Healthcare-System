from datetime import datetime

def audit_agent(state: dict):
    """
    Audit Agent:
    Logs all workflow actions and decisions with timestamps.
    """

    audit_log = state.get("audit_log") or []

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "raw_input": state.get("raw_input"),
        "structured_data": state.get("structured_data"),
        "validated": state.get("validated"),
        "issues": state.get("issues", []),
        "decision": state.get("decision"),
        "actions": state.get("actions", [])
    }

    audit_log.append(entry)

    print("[Audit Agent] Logging workflow step...")
    return {"audit_log": audit_log}
