from kubernetes import client, config

def get_pods():
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    namespace = open(
        "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    ).read().strip()

    pods = v1.list_namespaced_pod(namespace)

    result = []

    for pod in pods.items:
        result.append({
            "name": pod.metadata.name,
            "status": pod.status.phase
        })

    return result
