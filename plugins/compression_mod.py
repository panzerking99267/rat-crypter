def register(app):
    import os
    import zipfile
    from tkinter import filedialog, messagebox

    def compress_files():
        files = filedialog.askopenfilenames(title="Select files to compress")
        if not files:
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("Zip Archives", "*.zip")],
            title="Save compressed archive as"
        )
        if not out:
            return
        try:
            with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
                for file in files:
                    archive.write(file, os.path.basename(file))
            messagebox.showinfo("Compression", f"Files compressed to {os.path.basename(out)}")
        except Exception as e:
            messagebox.showerror("Compression Error", str(e))
    app.add_tools_menu("Compress Files (.zip)", compress_files)