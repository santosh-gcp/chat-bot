from k8s import (
    get_pods,
    get_nodes,
    get_services,
    get_deployments,
    get_events,
    get_namespaces
)

def chatbot(question: str):
    question = question.lower()

    if "pod" in question:
        return get_pods()

    elif "deployment" in question:
        return get_deployments()

    elif "service" in question:
        return get_services()

    elif "event" in question:
        return get_events()

    elif "node" in question:
        return get_nodes()

    elif "namespace" in question:
        return get_namespaces()

    return {
        "answer": "Sorry, I don't understand that question yet."
    }
