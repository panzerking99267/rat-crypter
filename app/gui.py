import tkinter as tk
from tkinter import ttk

class UltimateCrypterGUI:
    def __init__(self, core_app):
        self.app = core_app
        self.root = tk.Tk()
        self.root.title("Ultimate Crypter 2025")
        self.setup_gui()
        self.tools_menu = None

    def setup_gui(self):
        sidebar = tk.Frame(self.root, bg="#222", width=180)
        sidebar.pack(side="left", fill="y")
        tk.Label(sidebar, text="Ultimate Crypter", fg="#fff", bg="#222", font=("Segoe UI", 16, "bold")).pack(pady=20)
        # Placeholders for navigation
        self.main_area = tk.Frame(self.root, bg="#2a2a35")
        self.main_area.pack(side="right", expand=True, fill="both")
        # Tools menu for mods
        self.tools_menu = tk.Menu(self.root, tearoff=0)
        menubar = tk.Menu(self.root)
        menubar.add_cascade(label="Tools", menu=self.tools_menu)
        self.root.config(menu=menubar)

    def add_tools_menu(self, label, command):
        self.tools_menu.add_command(label=label, command=command)

    def run(self):
        self.root.mainloop()