from kubernetes import client, config
import npyscreen


class PodSelectorForm(npyscreen.FormBaseNew):
    def create(self):
        self.keypress_timeout = 10
        self.add_handlers({"b": self.onBack})
        self.selected_pods = []

        self.pod_update_id = -1
        self.pod_list = self.add(
            npyscreen.MultiSelect, scroll_exit=True, name="Pods", values=["Loading"]
        )

    def while_waiting(self):
        (id, pods) = self.parentApp.model.pods
        if self.pod_update_id == id:
            return None

        self.pod_update_id = id
        self.pods = pods
        pod_names = [i.metadata.name for i in self.pods]
        self.pod_list.values = pod_names
        self.display()

    def onBack(self, *args, **keywords):
        self.selected_pods = []

        for i in self.pod_list.value:
            self.selected_pods.append(self.pods[i])

        self.parentApp.switchFormPrevious()
