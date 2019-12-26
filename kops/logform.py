from kubernetes import client, config
import npyscreen


class PodInputList(npyscreen.TitleMultiLine):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.onChange = keywords["onChanged"]

    def when_value_edited(self):
        self.onChange()


class LogForm(npyscreen.FormBaseNew):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.add_handlers({"q": self.onQuit})

        self.v1 = client.CoreV1Api()
        self.pods = self.v1.list_pod_for_all_namespaces(watch=False).items

        pod_names = [i.metadata.name for i in self.pods]

        self.pod_list = self.add(
            PodInputList,
            scroll_exit=True,
            height=5,
            name="Pods",
            values=pod_names,
            onChanged=self.onChange,
        )
        self.text = self.add(
            npyscreen.TitleMultiLine,
            scroll_exit=True,
            name="Logs",
            values=str(self.pods[0].to_str).split("\n"),
        )

    def onChange(self):
        index = self.pod_list.value
        if index is None:
            return

        pod = self.pods[index]
        log = self.v1.read_namespaced_pod_log(
            name=pod.metadata.name, namespace=pod.metadata.namespace, tail_lines=60
        )

        self.text.set_values(log.split("\n"))
        self.text.update()

    def onQuit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
