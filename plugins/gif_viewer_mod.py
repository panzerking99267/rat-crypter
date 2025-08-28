def register(app):
    try:
        from PIL import Image, ImageTk, ImageSequence
    except ImportError:
        from tkinter import messagebox
        messagebox.showerror("Missing Pillow", "Install Pillow (pip install pillow) for GIF support!")
        return
    import os
    from tkinter import Toplevel, filedialog, Label

    def show_gif():
        file = filedialog.askopenfilename(title="Select GIF", filetypes=[("GIF files", "*.gif")])
        if not file:
            return
        win = Toplevel(app.root)
        win.title("GIF Viewer")
        lbl = Label(win)
        lbl.pack()
        gif = Image.open(file)
        frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

        def animate(idx=0):
            lbl.config(image=frames[idx])
            win.after(80, animate, (idx+1)%len(frames))
        animate()
        win.geometry(f"{gif.width}x{gif.height+20}")

    app.add_tools_menu("🖼️ View GIF", show_gif)