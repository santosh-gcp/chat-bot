from kubernetes import client, config

def get_pods():
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
        namespace = f.read().strip()

    pods = v1.list_namespaced_pod(namespace)

    result = []

    for pod in pods.items:

        # Skip build pods
        if "-build" in pod.metadata.name:
            continue

        result.append({
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
            "ip": pod.status.pod_ip
        })

    return result
