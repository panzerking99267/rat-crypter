def register(app):
    import hashlib
    from tkinter import filedialog, messagebox

    def hash_file():
        file = filedialog.askopenfilename(title="Select a file to hash")
        if not file:
            return
        try:
            with open(file, "rb") as f:
                data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            sha256 = hashlib.sha256(data).hexdigest()
            messagebox.showinfo(
                "File Hashes",
                f"MD5: {md5}\nSHA256: {sha256}"
            )
        except Exception as e:
            messagebox.showerror("Hash Error", str(e))
    app.add_tools_menu("Hash File (MD5/SHA256)", hash_file)