import npyscreen

from .kubernetesmodel import KubernetesModel
from .logform import LogForm


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.model = KubernetesModel()
        self.model.start()
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", LogForm, name="kops")
