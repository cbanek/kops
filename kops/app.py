import npyscreen

from .logform import LogForm


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("MAIN", LogForm, name="kops")
