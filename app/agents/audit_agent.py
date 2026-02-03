import json
from datetime import datetime
import os

AUDIT_LOG_FILE = "audit_logs.json"

def audit_agent(state: dict):
    """
    Audit Agent:
    Logs the workflow step with timestamp, state, decisions, and actions.
    Stores logs in a persistent JSON file.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "raw_input": state.get("raw_input"),
        "structured_data": state.get("structured_data"),
        "validated": state.get("validated"),
        "issues": state.get("issues", []),
        "decision": state.get("decision"),
        "actions": state.get("actions", [])
    }

    # Load existing logs
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, "r") as f:
            try:
                audit_logs = json.load(f)
            except json.JSONDecodeError:
                audit_logs = []
    else:
        audit_logs = []

    # Append new log
    audit_logs.append(log_entry)

    # Save updated logs
    with open(AUDIT_LOG_FILE, "w") as f:
        json.dump(audit_logs, f, indent=2)

    print("[Audit Agent] Logging workflow step...")

    return {"audit_log": audit_logs}
