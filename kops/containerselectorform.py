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

    def sort(self, item):
        return item.key

    def while_waiting(self):
        (id, pods) = self.parentApp.model.pods

        if self.pod_update_id == id:
            return None

        # Build the tree, and collate namespaces.
        namespaces = {}
        r = npyscreen.TreeData(selectable=False, ignore_root=True)
        r.sort = True
        r.sort_function_wrapper = False
        r.sort_function = self.sort

        for p in pods:
            namespace = namespaces.get(p.metadata.namespace, None)
            if namespace is None:
                namespace = r.new_child(content=p.metadata.namespace)
                namespaces[p.metadata.namespace] = namespace
            namespace.key = p.metadata.namespace

            pod = namespace.new_child(content=p.metadata.name)
            if len(p.spec.containers) == 1:
                pod.data = p
                pod.key = '.'.join([namespace.key, p.metadata.name, p.spec.containers[0].name])
            else:
                pod.key = '.'.join([namespace.key, p.metadata.name])
                for container in p.spec.containers:
                    c = pod.new_child(content=container.name)
                    c.key = '.'.join([namespace.key, p.metadata.name, container.name])
                    p_copy = copy.deepcopy(p)
                    p_copy.spec.containers = [container]
                    c.data = p_copy

        # Here we copy over what was selected before to the new tree.
        # We use the key property for this, which allows us to figure out
        # which items are set, and set them in the new tree.  If a node is
        # selected, select all the items below it using the walk_tree.
        # So if a namespace is selected and gets a new pod, select that.
        selected_keys = [i.key for i in self.tree.get_selected_objects()]

        for i in r.walk_tree():
            if i.key in selected_keys:
                for j in i.walk_tree(ignore_root=False):
                    j.selected = True

        # Update and redraw.
        self.tree.values = r
        self.tree.display()
        self.pod_update_id = id

    def onBack(self, *args, **keywords):
        self.selected_containers = []

        for obj in self.tree.get_selected_objects():
            # Only leaf nodes that are containers
            # (or pods with just 1 container) have a data property.
            if hasattr(obj, 'data'):
                self.selected_containers.append(obj.data)

        self.parentApp.switchFormPrevious()
