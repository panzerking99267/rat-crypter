def register(app):
    import random
    from tkinter import messagebox

    QUOTES = [
        "Stay curious, stay secure!",
        "Encryption is freedom.",
        "Obfuscate all the things.",
        "You can never have enough entropy.",
        "Don't forget to back up your keys!",
        "A strong password is your best friend.",
        "Keep learning, keep coding.",
        "Privacy is not a crime.",
    ]

    def show_quote():
        messagebox.showinfo("Crypto Quote", random.choice(QUOTES))
    app.add_tools_menu("Show Random Crypto Quote", show_quote)