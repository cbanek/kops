from kubernetes import client, config
import npyscreen

class PodInputList(npyscreen.TitleMultiLine):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.onChange = keywords['onChanged']

    def when_value_edited(self):
        self.onChange()

class MainForm(npyscreen.FormBaseNew):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.add_handlers({'q': self.onQuit})

        self.v1 = client.CoreV1Api()
        ret = self.v1.list_pod_for_all_namespaces(watch=False)

        self.pod_names = [i.metadata.name for i in ret.items]
        self.namespaces = [i.metadata.namespace for i in ret.items]

        self.pod_list = self.add(PodInputList, scroll_exit=True, height=5, name='Pods', values=self.pod_names, onChanged=self.onChange)
        self.text = self.add(npyscreen.TitleMultiLine, scroll_exit=True, name='Logs', values=[])

    def onChange(self):
        index = self.pod_list.value
        if index is None:
            return
        log = self.v1.read_namespaced_pod_log(name=self.pod_names[index], namespace=self.namespaces[index], tail_lines=60)
        self.text.set_values(log.split('\n'))
        self.text.update()

    def onQuit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm('MAIN', MainForm, name='kops')

if __name__ == '__main__':
    config.load_kube_config()
    App = Application().run()
