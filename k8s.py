from kubernetes import client, config

def get_pods():
    # Load in-cluster configuration
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    # Read current namespace
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
        namespace = f.read().strip()

    pods = v1.list_namespaced_pod(namespace)

    result = []

    for pod in pods.items:
        result.append({
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
            "ip": pod.status.pod_ip
        })

    return result
