from app.services.llm import llm
import json

def reasoning_agent(state: dict):
    validated = state.get("validated", True)
    issues = state.get("issues", [])

    prompt = f"""
You are an AI workflow decision-maker in a healthcare automation system.

Given:
- validated: {validated}
- issues: {issues}

Decide the next action in the workflow. Options:
- "request_missing_info" (if validated is False)
- "proceed_to_scheduling" (if validated is True)
- "flag_for_manual_review" (if there are serious issues)

IMPORTANT:
- Return ONLY a JSON object with one key: "decision"
- Do NOT include any text outside the JSON
- Example:
{{"decision": "request_missing_info"}}

JSON only:
"""

    response = llm.invoke(prompt)

    # Try parsing JSON
    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        # Strip leading/trailing characters and try again
        import re
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group())
            except json.JSONDecodeError:
                result = {"decision": "manual_review_due_to_parsing_error"}
        else:
            result = {"decision": "manual_review_due_to_parsing_error"}

    return result
