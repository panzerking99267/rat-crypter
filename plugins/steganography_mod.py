def register(app):
    def hide_in_image():
        from tkinter import filedialog, messagebox
        try:
            from PIL import Image
        except ImportError:
            messagebox.showerror("Missing Pillow", "Install Pillow for steganography support!")
            return
        img_path = filedialog.askopenfilename(title="Select PNG Image", filetypes=[("PNG Images","*.png")])
        if not img_path: return
        payload_path = filedialog.askopenfilename(title="Select Payload File")
        if not payload_path: return
        out_path = filedialog.asksaveasfilename(title="Save Stego Image", defaultextension=".png")
        if not out_path: return
        # Hide payload by appending as bytes (simplest stego)
        try:
            with open(img_path, "rb") as imgf, open(payload_path, "rb") as payf:
                img_data = imgf.read()
                payload = payf.read()
            with open(out_path, "wb") as outf:
                outf.write(img_data)
                outf.write(b"STEGO_PAYLOAD" + payload)
            messagebox.showinfo("Stego", "Payload hidden in image! (demo, not secure)")
        except Exception as e:
            messagebox.showerror("Stego Error", str(e))
    app.add_tools_menu("Steganography: Hide File in Image", hide_in_image)
