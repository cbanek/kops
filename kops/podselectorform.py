from kubernetes import client, config
import npyscreen


class PodSelectorForm(npyscreen.FormBaseNew):
    def create(self):
        self.keypress_timeout = 10
        self.add_handlers({"b": self.onBack})
        self.selected_pods = []

        self.pod_update_id = -1
        self.tree = self.add(npyscreen.MLTreeMultiSelect)

    def while_waiting(self):
        (id, pods) = self.parentApp.model.pods

        if self.pod_update_id == id:
            return None

        child_namespaces = {}
        child_pods = {}
        r = npyscreen.TreeData(selectable=False, ignore_root=True)

        for p in pods:
            namespace = child_namespaces.get(p.metadata.namespace, None)

            if namespace is None:
                namespace = r.new_child(content=p.metadata.namespace)
                child_namespaces[p.metadata.namespace] = namespace

            pod = child_pods.get(p.metadata.name, None)

            if pod is None:
                pod = namespace.new_child(content=p.metadata.name)
                child_pods[p.metadata.name] = pod

            if len(p.spec.containers) > 1:
                for container in p.spec.containers:
                    pod.new_child(content=container.name)

        self.tree.values = r
        self.pod_update_id = id

    def onBack(self, *args, **keywords):
        self.selected_pods = []
        self.parentApp.switchFormPrevious()
