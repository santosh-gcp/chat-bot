from k8s import (
    get_pods,
    get_nodes,
    get_services,
    get_deployments,
    get_events,
    get_namespaces,
)

def chatbot(question: str):

    q = question.lower()

    if any(word in q for word in [
        "pod",
        "pods",
        "running pods",
        "failed pods",
        "show pods"
    ]):
        return {
            "answer": get_pods()
        }

    elif any(word in q for word in [
        "deployment",
        "deployments",
        "apps"
    ]):
        return {
            "answer": get_deployments()
        }

    elif any(word in q for word in [
        "service",
        "services"
    ]):
        return {
            "answer": get_services()
        }

    elif any(word in q for word in [
        "event",
        "events",
        "warning"
    ]):
        return {
            "answer": get_events()
        }

    elif any(word in q for word in [
        "node",
        "nodes"
    ]):
        return {
            "answer": get_nodes()
        }

    elif any(word in q for word in [
        "namespace",
        "namespaces",
        "project"
    ]):
        return {
            "answer": get_namespaces()
        }

    return {
        "answer": "Sorry, I don't know how to answer that yet."
    }
