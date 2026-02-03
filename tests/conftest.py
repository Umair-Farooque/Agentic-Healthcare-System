import pytest
from app.graph.workflow_graph import build_workflow_graph

@pytest.fixture
def workflow_graph():
    return build_workflow_graph()

@pytest.fixture
def sample_patient_text():
    return "Patient Jane Doe, 30 years old, reporting severe headaches and nausea."
