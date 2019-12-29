from kubernetes import client, config
import npyscreen

from .containerselectorform import ContainerSelectorForm


class LogForm(npyscreen.FormBaseNew):
    def create(self):
        self.add_handlers({"b": self.onBack})
        self.add_handlers({"s": self.onSelect})

        self.v1 = client.CoreV1Api()
        self.text = self.add(
            npyscreen.TitleMultiLine, scroll_exit=True, name="Logs", values=[]
        )
        self.selector = self.parentApp.addForm(
            "container-selector", ContainerSelectorForm, name="Select containers"
        )
        self.keypress_timeout = 10

    def while_waiting(self):
        self.containers = self.selector.selected_containers

        if not self.containers:
            return

        pod = self.containers[0]
        log = self.v1.read_namespaced_pod_log(
            name=pod.metadata.name,
            namespace=pod.metadata.namespace,
            container=pod.spec.containers[0].name,
            tail_lines=60
        )

        self.text.set_values(log.split("\n"))
        self.text.update()

    def onSelect(self, *args, **keywords):
        self.parentApp.switchForm("container-selector")

    def onBack(self, *args, **keywords):
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormPrevious()
