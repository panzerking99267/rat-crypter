def register(app):
    try:
        from PyPDF2 import PdfWriter, PdfReader
    except ImportError:
        from tkinter import messagebox
        messagebox.showerror("Missing PyPDF2", "Install PyPDF2 for PDF protection mod!")
        return
    from tkinter import filedialog, simpledialog, messagebox

    def protect_pdf():
        file = filedialog.askopenfilename(title="Select PDF to protect", filetypes=[("PDF Files","*.pdf")])
        if not file:
            return
        password = simpledialog.askstring("Set PDF Password", "Password for PDF encryption:", show="*")
        if not password:
            return
        try:
            reader = PdfReader(file)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            out = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save protected PDF")
            if not out:
                return
            with open(out, "wb") as outf:
                writer.write(outf)
            messagebox.showinfo("PDF Protected", f"PDF encrypted and saved as {out}")
        except Exception as e:
            messagebox.showerror("PDF Protection Error", str(e))
    app.add_tools_menu("Encrypt/Protect PDF", protect_pdf)