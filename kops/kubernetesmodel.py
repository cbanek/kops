import kubernetes


class KubernetesModel:
    def __init__(self):
        self.api = kubernetes.client.CoreV1Api()
        self.watch = kubernetes.watch.Watch()
        self.pods = []

    def poll(self):
        for event in self.watch.stream(
            self.api.list_pod_for_all_namespaces, timeout_seconds=1
        ):
            action = event["type"]
            kind = event["object"].kind
            name = event["object"].metadata.name
            namespace = event["object"].metadata.namespace

            if action == "ADDED":
                if kind == "Pod":
                    self.pods.append({"name": name, "namespace": namespace})
            if action == "DELETED":
                if kind == "Pod":
                    self.pods.remove({"name": name, "namespace": namespace})
