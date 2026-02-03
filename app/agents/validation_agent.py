from app.services.llm import llm
import json

def validation_agent(state: dict):
    """
    LLM-powered Validation Agent:
    - Checks structured_data from Intake Agent
    - Flags missing or inconsistent fields
    - Returns validated flag and optional issues
    """

    structured = state.get("structured_data", {})

    prompt = f"""
You are a healthcare data validator.

Given the following structured patient data in JSON:
{json.dumps(structured, indent=2)}

Check for the following:
1. Missing required fields (patient_name, age, symptoms, diagnosis)
2. Inconsistent values (e.g., age not a number, symptoms not a list)
3. Any other potential issues

Return ONLY JSON in the format:
{{
  "validated": true or false,
  "issues": ["list of issues found"]
}}
"""

    # Call the LLM
    response = llm.invoke(prompt)

    # Parse safely
    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        result = {"validated": False, "issues": ["Could not parse LLM output", response]}

    return result
