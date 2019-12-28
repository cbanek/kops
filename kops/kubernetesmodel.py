import threading

import kubernetes


class KubernetesModel:
    def __init__(self):
        self.api = kubernetes.client.CoreV1Api()
        self._pod_watch = kubernetes.watch.Watch()
        self._pods = []
        self._pod_update_id = 0

    def start(self):
        self._pod_thread_lock = threading.Lock()
        self._pod_thread = threading.Thread(target=self._watch_pods, daemon=True)
        self._pod_thread.start()

    def _watch_pods(self):
        for event in self._pod_watch.stream(self.api.list_pod_for_all_namespaces):
            action = event["type"]

            with self._pod_thread_lock:
                if action == "ADDED":
                    self._pods.append(event["object"])
                if action == "DELETED":
                    self._pods.remove(event["object"])

                self._pod_update_id += 1

    @property
    def pods(self):
        with self._pod_thread_lock:
            return (self._pod_update_id, list(self._pods))
