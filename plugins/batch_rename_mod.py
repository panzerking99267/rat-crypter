def register(app):
    import os
    from tkinter import filedialog, simpledialog, messagebox

    def batch_rename():
        folder = filedialog.askdirectory(title="Select folder with files to rename")
        if not folder:
            return
        prefix = simpledialog.askstring("Batch Rename", "Enter new filename prefix:", initialvalue="renamed_")
        if prefix is None:
            return
        count = 0
        try:
            for idx, fname in enumerate(os.listdir(folder)):
                path = os.path.join(folder, fname)
                if os.path.isfile(path):
                    ext = os.path.splitext(fname)[-1]
                    newname = f"{prefix}{idx+1}{ext}"
                    os.rename(path, os.path.join(folder, newname))
                    count += 1
            messagebox.showinfo("Batch Rename", f"Renamed {count} files.")
        except Exception as e:
            messagebox.showerror("Batch Rename Error", str(e))
    app.add_tools_menu("Batch Rename Files in Folder", batch_rename)