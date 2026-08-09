from kubernetes import client, config

# Load OpenShift in-cluster configuration
config.load_incluster_config()

core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
custom_objects = client.CustomObjectsApi()


def get_namespace():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
        return f.read().strip()


# ============================================================
# PODS
# ============================================================

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


# ============================================================
# POD HEALTH
# ============================================================

def get_unhealthy_pods():
    namespace = get_namespace()

    pods = core_v1.list_namespaced_pod(namespace)

    result = []

    for pod in pods.items:

        if "-build" in pod.metadata.name:
            continue

        phase = pod.status.phase

        # Basic unhealthy detection
        if phase not in ["Running", "Succeeded"]:
            result.append({
                "name": pod.metadata.name,
                "status": phase,
                "node": pod.spec.node_name,
                "reason": pod.status.reason
            })

    return result


# ============================================================
# DEPLOYMENTS
# ============================================================

def get_deployments():
    namespace = get_namespace()

    deployments = apps_v1.list_namespaced_deployment(namespace)

    result = []

    for deploy in deployments.items:

        result.append({
            "name": deploy.metadata.name,
            "desired_replicas": deploy.spec.replicas or 0,
            "ready_replicas": deploy.status.ready_replicas or 0,
            "available_replicas": deploy.status.available_replicas or 0,
            "updated_replicas": deploy.status.updated_replicas or 0
        })

    return result


# ============================================================
# SERVICES
# ============================================================

def get_services():
    namespace = get_namespace()

    services = core_v1.list_namespaced_service(namespace)

    result = []

    for svc in services.items:

        result.append({
            "name": svc.metadata.name,
            "type": svc.spec.type,
            "cluster_ip": svc.spec.cluster_ip,
            "ports": [
                p.port for p in svc.spec.ports
            ]
        })

    return result


# ============================================================
# EVENTS
# ============================================================

def get_events():
    namespace = get_namespace()

    events = core_v1.list_namespaced_event(namespace)

    result = []

    for event in events.items:

        result.append({
            "type": event.type,
            "reason": event.reason,
            "object": event.involved_object.name,
            "kind": event.involved_object.kind,
            "message": event.message
        })

    return result


# ============================================================
# WARNING EVENTS
# ============================================================

def get_warning_events():
    namespace = get_namespace()

    events = core_v1.list_namespaced_event(namespace)

    result = []

    for event in events.items:

        if event.type == "Warning":

            result.append({
                "reason": event.reason,
                "object": event.involved_object.name,
                "kind": event.involved_object.kind,
                "message": event.message
            })

    return result


# ============================================================
# NODES
# ============================================================

def get_nodes():

    try:
        nodes = core_v1.list_node()

        result = []

        for node in nodes.items:

            status = "Unknown"

            if node.status.conditions:
                for condition in node.status.conditions:

                    if condition.type == "Ready":

                        if condition.status == "True":
                            status = "Ready"
                        else:
                            status = "NotReady"

            result.append({
                "name": node.metadata.name,
                "status": status,
                "os": node.status.node_info.os_image,
                "kernel": node.status.node_info.kernel_version,
                "kubelet": node.status.node_info.kubelet_version
            })

        return result

    except Exception as e:

        return {
            "error": "Unable to access node information",
            "details": str(e)
        }


# ============================================================
# NAMESPACES
# ============================================================

def get_namespaces():

    try:

        namespaces = core_v1.list_namespace()

        result = []

        for ns in namespaces.items:

            result.append({
                "name": ns.metadata.name,
                "status": ns.status.phase
            })

        return result

    except Exception as e:

        return {
            "error": "Unable to access namespace information",
            "details": str(e)
        }


# ============================================================
# OPENSHIFT OPERATORS
# ============================================================

def get_cluster_operators():

    try:

        operators = custom_objects.list_cluster_custom_object(
            group="config.openshift.io",
            version="v1",
            plural="clusteroperators"
        )

        result = []

        for operator in operators.get("items", []):

            conditions = operator.get("status", {}).get(
                "conditions", []
            )

            available = "Unknown"
            progressing = "Unknown"
            degraded = "Unknown"

            for condition in conditions:

                condition_type = condition.get("type")
                status = condition.get("status")

                if condition_type == "Available":
                    available = status

                elif condition_type == "Progressing":
                    progressing = status

                elif condition_type == "Degraded":
                    degraded = status

            result.append({
                "name": operator.get("metadata", {}).get("name"),
                "available": available,
                "progressing": progressing,
                "degraded": degraded
            })

        return result

    except Exception as e:

        return {
            "error": "Unable to access ClusterOperators",
            "details": str(e)
        }


# ============================================================
# CLUSTER HEALTH SUMMARY
# ============================================================

def get_cluster_health():

    health = {
        "namespace": get_namespace()
    }

    # Pods
    try:
        pods = get_pods()

        health["total_pods"] = len(pods)

        unhealthy = get_unhealthy_pods()

        health["unhealthy_pods"] = unhealthy

    except Exception as e:

        health["pods_error"] = str(e)

    # Deployments
    try:

        deployments = get_deployments()

        health["deployments"] = deployments

        unhealthy_deployments = []

        for deployment in deployments:

            if (
                deployment["ready_replicas"]
                < deployment["desired_replicas"]
            ):
                unhealthy_deployments.append(deployment)

        health["unhealthy_deployments"] = unhealthy_deployments

    except Exception as e:

        health["deployments_error"] = str(e)

    # Warning events
    try:

        health["warning_events"] = get_warning_events()

    except Exception as e:

        health["events_error"] = str(e)

    # Nodes
    health["nodes"] = get_nodes()

    # Operators
    health["cluster_operators"] = get_cluster_operators()

    return health

def get_unhealthy_pods():
    namespace = get_namespace()

    pods = core_v1.list_namespaced_pod(namespace)

    result = []

    unhealthy_statuses = {
        "Pending",
        "Failed",
        "Unknown",
    }

    for pod in pods.items:

        # Skip OpenShift build pods
        if "-build" in pod.metadata.name:
            continue

        reasons = []

        # Check pod phase
        if pod.status.phase in unhealthy_statuses:
            reasons.append(
                f"Pod phase is {pod.status.phase}"
            )

        # Check container statuses
        container_statuses = []

        if pod.status.container_statuses:
            container_statuses = pod.status.container_statuses

        for container in container_statuses:

            # Container not ready
            if container.ready is False:

                reasons.append(
                    f"Container {container.name} is not ready"
                )

            # Restart count
            if container.restart_count and container.restart_count > 3:

                reasons.append(
                    f"Container {container.name} restarted "
                    f"{container.restart_count} times"
                )

            # Container state
            if container.state:

                if container.state.waiting:

                    reason = container.state.waiting.reason

                    if reason:
                        reasons.append(
                            f"Container {container.name}: {reason}"
                        )

                if container.state.terminated:

                    reason = container.state.terminated.reason

                    if reason:
                        reasons.append(
                            f"Container {container.name}: {reason}"
                        )

        # Only return unhealthy pods
        if reasons:

            result.append({
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "pod_ip": pod.status.pod_ip,
                "restarts": sum(
                    c.restart_count
                    for c in container_statuses
                ),
                "reasons": reasons
            })

    return result
