from .gui import UltimateCrypterGUI
from .plugins import load_plugins

class UltimateCrypterApp:
    def __init__(self):
        self.gui = UltimateCrypterGUI(self)
        load_plugins(self)

    def add_tools_menu(self, label, command):
        self.gui.add_tools_menu(label, command)

    def run(self):
        self.gui.run()