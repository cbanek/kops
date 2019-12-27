from kubernetes import client, config
import npyscreen

from .podselectorform import PodSelectorForm


class LogForm(npyscreen.FormBaseNew):
    def create(self):
        self.add_handlers({"b": self.onBack})
        self.add_handlers({"s": self.onSelect})

        self.v1 = client.CoreV1Api()
        self.text = self.add(
            npyscreen.TitleMultiLine, scroll_exit=True, name="Logs", values=[]
        )
        self.selector = self.parentApp.addForm("pod-selector", PodSelectorForm)
        self.keypress_timeout = 10

    def while_waiting(self):
        self.pods = self.selector.selected_pods

        if not self.pods:
            return

        pod = self.pods[0]
        log = self.v1.read_namespaced_pod_log(
            name=pod.metadata.name, namespace=pod.metadata.namespace, tail_lines=60
        )

        self.text.set_values(log.split("\n"))
        self.text.update()

    def onSelect(self, *args, **keywords):
        self.parentApp.switchForm("pod-selector")

    def onBack(self, *args, **keywords):
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormPrevious()
