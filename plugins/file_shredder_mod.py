def register(app):
    import os
    import random
    from tkinter import filedialog, messagebox

    def shred_file():
        file = filedialog.askopenfilename(title="Select file to shred")
        if not file:
            return
        try:
            size = os.path.getsize(file)
            with open(file, "wb") as f:
                for _ in range(3):  # Overwrite 3 times
                    f.seek(0)
                    f.write(os.urandom(size))
            os.remove(file)
            messagebox.showinfo("Shredder", "File shredded and deleted!")
        except Exception as e:
            messagebox.showerror("Shredder Error", str(e))
    app.add_tools_menu("Shred (Secure Delete) File", shred_file)