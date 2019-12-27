from kubernetes import client, config
import npyscreen


class PodSelectorForm(npyscreen.FormBaseNew):
    def create(self):
        self.add_handlers({"b": self.onBack})

        self.v1 = client.CoreV1Api()
        self.pods = self.v1.list_pod_for_all_namespaces(watch=False).items

        pod_names = [i.metadata.name for i in self.pods]

        self.pod_list = self.add(
            npyscreen.MultiSelect, scroll_exit=True, name="Pods", values=pod_names
        )
        self.selected_pods = []

    def onBack(self, *args, **keywords):
        self.selected_pods = []

        for i in self.pod_list.value:
            self.selected_pods.append(self.pods[i])

        self.parentApp.switchFormPrevious()
