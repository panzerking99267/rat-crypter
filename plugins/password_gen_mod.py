def register(app):
    import random
    import string
    from tkinter import simpledialog, messagebox

    def generate_password():
        length = simpledialog.askinteger("Password Generator", "Length of password?", initialvalue=16, minvalue=4, maxvalue=128)
        if not length:
            return
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}:;,.<>/?"
        password = ''.join(random.choice(chars) for _ in range(length))
        app.root.clipboard_clear()
        app.root.clipboard_append(password)
        messagebox.showinfo("Password Generated", f"Password copied to clipboard:\n\n{password}")
    app.add_tools_menu("Generate Secure Password", generate_password)