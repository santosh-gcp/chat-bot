from kubernetes import client, config

config.load_incluster_config()

v1 = client.CoreV1Api()

def get_pods(namespace):
    pods = v1.list_namespaced_pod(namespace=namespace)

    result = []

    for pod in pods.items:
        result.append({
            "name": pod.metadata.name,
            "status": pod.status.phase
        })

    return result
