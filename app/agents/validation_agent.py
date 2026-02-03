from app.services.llm import llm

# Example ICD-10 codes for demonstration
ICD10_CODES = ["I20", "I21", "J45", "E11"]  

def validation_agent(state: dict):
    """
    Validation Agent:
    - Checks structured data for missing fields and correctness.
    - Flags critical issues (e.g., high-risk symptoms).
    """
    data = state.get("structured_data", {})
    issues = []

    # Check basic fields
    patient_name = data.get("patient_name")
    age = data.get("age")
    symptoms = data.get("symptoms", [])
    diagnosis = data.get("diagnosis", "")
    missing_info = data.get("missing_info", [])

    if not patient_name:
        issues.append("Patient name missing")
    if not isinstance(age, int) or age <= 0 or age > 120:
        issues.append(f"Invalid age: {age}")
    if not symptoms:
        issues.append("Symptoms missing")
    if not diagnosis:
        issues.append("Diagnosis missing")
    if missing_info:
        issues.extend([f"Missing info: {field}" for field in missing_info])

    # Critical symptom detection (simplified example)
    high_risk_symptoms = ["chest pain", "shortness of breath", "unconscious"]
    for symptom in symptoms:
        if symptom.lower() in high_risk_symptoms:
            issues.append(f"Critical symptom detected: {symptom}")

    # Optional: use LLM to check consistency / reasoning
    llm_prompt = f"""
Validate the patient data and list any inconsistencies or missing important info.
Patient Data: {data}
"""
    llm_response = llm.invoke(llm_prompt)
    # Optionally parse LLM response and append to issues
    issues.append(f"LLM check: {llm_response}")

    validated = len(issues) == 0

    return {
        "validated": validated,
        "issues": issues
    }
