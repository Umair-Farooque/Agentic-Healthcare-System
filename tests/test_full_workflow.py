from app.agents.intake_agent import intake_agent
from app.agents.validation_agent import validation_agent
from app.agents.reasoning_agent import reasoning_agent
from app.agents.action_agent import action_agent
from app.agents.audit_agent import audit_agent

# ---------------- Sample Input ----------------
sample_input = {
    "raw_input": "Patient John Doe, 55 years old, complains of chest pain and shortness of breath. Suspected angina. Insurance ID missing.",
    # Optional file input for PDF / OCR
    "file_input": None
}

# ---------------- Step 1: Intake ----------------
state = intake_agent(sample_input)
print("\n[Intake Agent] Structured Data:")
print(state["structured_data"])

# ---------------- Step 2: Validation ----------------
validation_results = validation_agent(state)
state.update(validation_results)
print("\n[Validation Agent] Results:")
print(validation_results)

# ---------------- Step 3: Reasoning ----------------
reasoning_results = reasoning_agent(state)
state.update(reasoning_results)
print("\n[Reasoning Agent] Decision:")
print(reasoning_results)

# ---------------- Step 4: Action ----------------
action_results = action_agent(state)
state.update(action_results)
print("\n[Action Agent] Actions Taken:")
print(action_results)

# ---------------- Step 5: Audit ----------------
audit_results = audit_agent(state)
print("\n[Audit Agent] Last Audit Log Entry:")
print(audit_results["audit_log"][-1])
