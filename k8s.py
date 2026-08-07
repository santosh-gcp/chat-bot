from kubernetes import client, config

# Load OpenShift in-cluster configuration
config.load_incluster_config()

core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


def get_namespace():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
        return f.read().strip()


############################################
# PODS
############################################

def get_pods():
    namespace = get_namespace()

    pods = core_v1.list_namespaced_pod(namespace)

    result = []

    for pod in pods.items:

        # Skip OpenShift build pods
        if "-build" in pod.metadata.name:
            continue

        result.append({
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
            "pod_ip": pod.status.pod_ip,
            "host_ip": pod.status.host_ip
        })

    return result


############################################
# DEPLOYMENTS
############################################

def get_deployments():
    namespace = get_namespace()

    deployments = apps_v1.list_namespaced_deployment(namespace)

    result = []

    for deploy in deployments.items:

        result.append({
            "name": deploy.metadata.name,
            "desired_replicas": deploy.spec.replicas,
            "ready_replicas": deploy.status.ready_replicas,
            "available_replicas": deploy.status.available_replicas
        })

    return result


############################################
# SERVICES
############################################

def get_services():
    namespace = get_namespace()

    services = core_v1.list_namespaced_service(namespace)

    result = []

    for svc in services.items:

        result.append({
            "name": svc.metadata.name,
            "type": svc.spec.type,
            "cluster_ip": svc.spec.cluster_ip,
            "ports": [p.port for p in svc.spec.ports]
        })

    return result


############################################
# EVENTS
############################################

def get_events():
    namespace = get_namespace()

    events = core_v1.list_namespaced_event(namespace)

    result = []

    for event in events.items:

        result.append({
            "type": event.type,
            "reason": event.reason,
            "object": event.involved_object.name,
            "message": event.message
        })

    return result


############################################
# NODES
############################################

def get_nodes():

    nodes = core_v1.list_node()

    result = []

    for node in nodes.items:

        status = "Unknown"

        for condition in node.status.conditions:
            if condition.type == "Ready":
                status = condition.status

        result.append({
            "name": node.metadata.name,
            "status": status,
            "os": node.status.node_info.os_image,
            "kernel": node.status.node_info.kernel_version,
            "kubelet": node.status.node_info.kubelet_version
        })

    return result


############################################
# NAMESPACES
############################################

def get_namespaces():

    namespaces = core_v1.list_namespace()

    result = []

    for ns in namespaces.items:

        result.append({
            "name": ns.metadata.name,
            "status": ns.status.phase
        })

    return result
