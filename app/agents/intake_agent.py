from app.services.llm import llm
import json

def intake_agent(state: dict):
    raw_text = state.get("raw_input", "")

    prompt = f"""
Extract the following information and return ONLY JSON with keys:
- patient_name (string)
- age (integer)
- symptoms (list of strings)
- diagnosis (string)
- missing_info (list of missing fields)

Text:
\"\"\"{raw_text}\"\"\"
"""

    # Correct: use invoke() instead of calling llm()
    response = llm.invoke(prompt)

    # Parse JSON safely
    try:
        structured_data = json.loads(response)
    except json.JSONDecodeError:
        structured_data = {"error": "JSON parse failed", "raw_output": response}

    return {"structured_data": structured_data}
