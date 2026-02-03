from typing import List
from langgraph.graph import StateGraph, START, END
from app.graph.state_schema import WorkflowState

# agent functions
from app.agents.intake_agent import intake_agent
from app.agents.validation_agent import validation_agent
from app.agents.reasoning_agent import reasoning_agent
from app.agents.action_agent import action_agent
from app.agents.audit_agent import audit_agent

def build_workflow_graph():
    builder = StateGraph(WorkflowState)

    # Add nodes
    builder.add_node("intake", intake_agent)
    builder.add_node("validate", validation_agent)
    builder.add_node("reason", reasoning_agent)
    builder.add_node("act", action_agent)
    builder.add_node("audit", audit_agent)

    # Define flow
    builder.add_edge(START, "intake")
    builder.add_edge("intake", "validate")
    builder.add_edge("validate", "reason")
    builder.add_edge("reason", "act")
    builder.add_edge("act", "audit")
    builder.add_edge("audit", END)

    # Compile
    graph = builder.compile()
    return graph
