def register(app):
    from tkinter import messagebox, Toplevel, Label, PhotoImage
    import os

    def hello_kitty():
        try:
            # Try to find a hello kitty image in plugins folder
            img_path = os.path.join("plugins", "hello_kitty.png")
            if os.path.isfile(img_path):
                win = Toplevel(app.root)
                win.title("Hello Kitty!")
                img = PhotoImage(file=img_path)
                lbl = Label(win, image=img, bg="pink")
                lbl.img = img
                lbl.pack()
                txt = Label(win, text="Hello Kitty Loves Encryption! 🐱💖", bg="pink", fg="#a23", font=("Comic Sans MS", 14, "bold"))
                txt.pack()
                win.configure(bg="pink")
                win.geometry(f"{img.width()}x{img.height()+40}")
            else:
                messagebox.showinfo("Hello Kitty!", "Hello Kitty Loves Encryption! 🐱💖")
        except Exception:
            messagebox.showinfo("Hello Kitty!", "Hello Kitty Loves Encryption! 🐱💖")
    app.add_tools_menu("🐱 Hello Kitty!", hello_kitty)