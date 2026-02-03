from typing import TypedDict, List

class WorkflowState(TypedDict):
    # the raw input text
    raw_input: str
    # structured parsed fields
    structured_data: dict
    # validation results
    validated: bool
    # next decision
    decision: str
    # actions taken
    actions: List[str]
    # audit log
    audit_log: List[str]
