import npyscreen

from .kubernetesmodel import KubernetesModel
from .logform import LogForm


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.model = KubernetesModel()
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", LogForm, name="kops")

    def while_waiting(self):
        self.model.poll()
