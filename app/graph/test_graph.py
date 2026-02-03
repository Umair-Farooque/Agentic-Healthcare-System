from app.graph.workflow_graph import build_workflow_graph

if __name__ == "__main__":
    graph = build_workflow_graph()

    sample_input = {
        "raw_input": "Patient John Doe, 55 years old, complains of chest pain and shortness of breath. Suspected angina. Insurance ID missing."
    }

    result = graph.invoke(sample_input)
    print("\nFinal State:")
    print(result)
