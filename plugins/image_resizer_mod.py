def register(app):
    try:
        from PIL import Image
    except ImportError:
        from tkinter import messagebox
        messagebox.showerror("Missing Pillow", "Install Pillow for image resizing mod!")
        return
    from tkinter import filedialog, simpledialog, messagebox

    def resize_image():
        file = filedialog.askopenfilename(title="Select image to resize", filetypes=[("Images","*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if not file:
            return
        width = simpledialog.askinteger("Resize Image", "New width (px)?", initialvalue=512)
        height = simpledialog.askinteger("Resize Image", "New height (px)?", initialvalue=512)
        if not width or not height:
            return
        try:
            img = Image.open(file)
            img = img.resize((width, height))
            out = filedialog.asksaveasfilename(defaultextension=".png", title="Save resized image")
            if not out:
                return
            img.save(out)
            messagebox.showinfo("Image Resizer", f"Resized image saved as {out}")
        except Exception as e:
            messagebox.showerror("Image Resize Error", str(e))
    app.add_tools_menu("Resize Image", resize_image)