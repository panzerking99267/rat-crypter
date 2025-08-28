def register(app):
    def hello():
        from tkinter import messagebox
        messagebox.showinfo("Hello Mod", "Hello from your mod!")
    app.add_tools_menu("Say Hello", hello)