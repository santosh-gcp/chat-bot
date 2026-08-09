from llm import ask_gpt
from k8s import (
    get_pods,
    get_unhealthy_pods,
    get_nodes,
    get_deployments,
    get_services,
    get_events,
    get_warning_events,
    get_namespaces,
    get_cluster_operators,
    get_cluster_health,
)

TOOLS = {
    "pods": get_pods,
    "unhealthy_pods": get_unhealthy_pods,
    "nodes": get_nodes,
    "deployments": get_deployments,
    "services": get_services,
    "events": get_events,
    "warning_events": get_warning_events,
    "namespaces": get_namespaces,
    "cluster_operators": get_cluster_operators,
    "cluster_health": get_cluster_health,
}


def chatbot(question: str):

    q = question.lower()
    
# Decide which Kubernetes tool to use
if (
    "unhealthy" in q
    or "failed pod" in q
    or "failed pods" in q
    or "pod health" in q
    or "pod status" in q
):
    data = get_unhealthy_pods()

elif "pod" in q or "pods" in q:
    data = get_pods()

elif "node" in q or "nodes" in q:
    data = get_nodes()

    # Decide which Kubernetes tool to use
    if "unhealthy pod" in q or "failed pod" in q or "pod health" in q:
        data = get_unhealthy_pods()

    elif "pod" in q:
        data = get_pods()

    elif "node" in q:
        data = get_nodes()

    elif "deployment" in q:
        data = get_deployments()

    elif "service" in q:
        data = get_services()

    elif "warning" in q or "warning event" in q:
        data = get_warning_events()

    elif "event" in q:
        data = get_events()

    elif "operator" in q:
        data = get_cluster_operators()

    elif "namespace" in q:
        data = get_namespaces()

    elif (
        "cluster health" in q
        or "cluster healthy" in q
        or "overall health" in q
        or "cluster status" in q
    ):
        data = get_cluster_health()

    else:
        return {
            "answer": ask_gpt(question)
        }

    # Ask the local LLM to explain the Kubernetes result
    prompt = f"""
You are an OpenShift cluster health assistant.

The user asked:

{question}

The following information was collected directly from the OpenShift cluster:

{data}

Answer the user's question using ONLY the information provided above.

Do not invent Kubernetes resources or statuses.

Be concise and clear.

If something is unhealthy, clearly mention:
- resource name
- current status
- likely issue if it is obvious from the data

If everything relevant is healthy, say so clearly.
"""

    answer = ask_gpt(prompt)

    return {
        "answer": answer,
        "data": data
    }
