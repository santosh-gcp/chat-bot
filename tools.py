from k8s import (
    get_pods,
    get_nodes,
    get_services,
    get_deployments,
    get_events,
    get_namespaces,
)

TOOLS = {
    "pods": get_pods,
    "deployments": get_deployments,
    "services": get_services,
    "events": get_events,
    "nodes": get_nodes,
    "namespaces": get_namespaces,
}
