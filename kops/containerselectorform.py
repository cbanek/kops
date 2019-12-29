import copy
import logging

from kubernetes import client, config
import npyscreen


class ContainerSelectorForm(npyscreen.FormBaseNew):
    def create(self):
        self.keypress_timeout = 10
        self.add_handlers({"b": self.onBack})
        self.selected_containers = []

        self.pod_update_id = -1
        self.tree = self.add(npyscreen.MLTreeMultiSelect)

    def while_waiting(self):
        (id, pods) = self.parentApp.model.pods

        if self.pod_update_id == id:
            return None

        namespaces = {}
        r = npyscreen.TreeData(selectable=False, ignore_root=True)

        for p in pods:
            namespace = namespaces.get(p.metadata.namespace, None)

            if namespace is None:
                namespace = r.new_child(content=p.metadata.namespace)
                namespaces[p.metadata.namespace] = namespace

            pod = namespace.new_child(content=p.metadata.name)
            if len(p.spec.containers) == 1:
                pod.data = p
            else:
                for container in p.spec.containers:
                    c = pod.new_child(content=container.name)
                    p_copy = copy.deepcopy(p)
                    p_copy.spec.containers = [container]
                    c.data = p_copy
                    

        self.tree.values = r
        self.pod_update_id = id
        self.tree.display()

    def onBack(self, *args, **keywords):
        self.selected_containers = []

        for obj in self.tree.get_selected_objects():
            # Only leaf nodes that are containers
            # (or pods with just 1 container) have a data property.
            if hasattr(obj, 'data'):
                self.selected_containers.append(obj.data)

        self.parentApp.switchFormPrevious()
