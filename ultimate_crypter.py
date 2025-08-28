import os, sys, importlib, traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import PhotoImage
from threading import Thread
import json

# Optional AES support
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Protocol.KDF import PBKDF2
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False

# Optional Pillow for steganography mod
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ---- Plugin System ----
PLUGIN_SAMPLE = """\
def register(app):
    def hello():
        from tkinter import messagebox
        messagebox.showinfo("Hello Mod", "Hello from your plugin mod!")
    app.add_tools_menu("Say Hello (Sample Mod)", hello)
"""

PLUGIN_STEGO = '''\
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
'''

def ensure_plugins():
    plugins_dir = "plugins"
    os.makedirs(plugins_dir, exist_ok=True)
    sample_path = os.path.join(plugins_dir, "sample_mod.py")
    if not os.path.isfile(sample_path):
        with open(sample_path, "w") as f:
            f.write(PLUGIN_SAMPLE)
    stego_path = os.path.join(plugins_dir, "steganography_mod.py")
    if not os.path.isfile(stego_path):
        with open(stego_path, "w") as f:
            f.write(PLUGIN_STEGO)

def load_plugins(app, plugins_dir="plugins"):
    if not os.path.isdir(plugins_dir):
        return
    sys.path.insert(0, plugins_dir)
    for fname in os.listdir(plugins_dir):
        if fname.endswith('.py') and fname != '__init__.py':
            modname = fname[:-3]
            try:
                module = importlib.import_module(modname)
                if hasattr(module, "register"):
                    module.register(app)
            except Exception as e:
                print(f"[Plugin Error] {fname}: {e}")
    sys.path.pop(0)

# ---- Encryption Logic ----
def xor_encrypt(data, key=0xAA):
    return bytes(b ^ key for b in data)

def aes_encrypt(data, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    encrypted = cipher.encrypt(data)
    return salt + iv + encrypted

# ---- Theme Data ----
THEMES = {
    "dark": {
        "bg": "#23232e",
        "panel": "#30304a",
        "fg": "#ffffff",
        "accent": "#FFD700",
        "button": "#393960",
        "button_fg": "#FFD700"
    },
    "light": {
        "bg": "#f6f6f6",
        "panel": "#e0e0ef",
        "fg": "#111",
        "accent": "#2a4e9b",
        "button": "#e4e4f8",
        "button_fg": "#2a4e9b"
    }
}

# ---- App Settings ----
SETTINGS_FILE = "crypter_settings.json"
DEFAULT_SETTINGS = {
    "theme": "dark",
    "encryption": "AES" if AES_AVAILABLE else "XOR"
}

def load_settings():
    if not os.path.isfile(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

# ---- Main GUI Class ----
class UltimateCrypterApp:
    def __init__(self):
        ensure_plugins()
        self.settings = load_settings()
        self.theme = self.settings.get("theme", "dark")
        self.encryption_method = self.settings.get("encryption", "AES" if AES_AVAILABLE else "XOR")
        self.file_list = []
        self.root = TkinterDnD.Tk()
        self.root.title("Ultimate Crypter 2025")
        self.root.geometry("1024x680")
        self.root.resizable(True, True)
        self.root['background'] = THEMES[self.theme]['bg']
        self.setup_gui()
        load_plugins(self)
        self.notify("Ultimate Crypter 2025 loaded!")

    def setup_gui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=THEMES[self.theme]['panel'], width=185)
        self.sidebar.pack(side="left", fill="y")
        tk.Label(self.sidebar, text="Ultimate Crypter", fg=THEMES[self.theme]['accent'], bg=THEMES[self.theme]['panel'], font=("Segoe UI", 18, "bold")).pack(pady=28)
        for label, func in [
            ("Dashboard", self.show_dashboard),
            ("Encrypt", self.show_encrypt),
            ("Settings", self.show_settings),
        ]:
            b = tk.Button(self.sidebar, text=label, bg=THEMES[self.theme]['button'], fg=THEMES[self.theme]['button_fg'], font=("Segoe UI", 13, "bold"), relief="flat", command=func)
            b.pack(fill="x", padx=18, pady=7)
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=THEMES[self.theme]['accent']))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg=THEMES[self.theme]['button']))

        # Main Area
        self.main_area = tk.Frame(self.root, bg=THEMES[self.theme]['bg'])
        self.main_area.pack(side="right", expand=True, fill="both")
        # Menu bar
        self.tools_menu = tk.Menu(self.root, tearoff=0)
        menubar = tk.Menu(self.root)
        menubar.add_cascade(label="Tools", menu=self.tools_menu)
        self.root.config(menu=menubar)
        # Drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        # Initial screen
        self.show_dashboard()

    # --- Theme management ---
    def apply_theme(self):
        t = THEMES[self.theme]
        self.root['background'] = t['bg']
        self.sidebar['bg'] = t['panel']
        for w in self.sidebar.winfo_children():
            try:
                if isinstance(w, tk.Label):
                    w.config(bg=t['panel'], fg=t['accent'])
                elif isinstance(w, tk.Button):
                    w.config(bg=t['button'], fg=t['button_fg'])
            except Exception: pass
        self.main_area['bg'] = t['bg']
        for w in self.main_area.winfo_children():
            try:
                w.config(bg=t['bg'])
            except Exception: pass

    def switch_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()
        self.settings['theme'] = self.theme
        save_settings(self.settings)

    # --- Plugin hooks ---
    def add_tools_menu(self, label, command):
        self.tools_menu.add_command(label=label, command=command)

    # --- Sidebar Navigation ---
    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def show_dashboard(self):
        self.clear_main()
        tk.Label(self.main_area, text="Dashboard", font=("Segoe UI", 22, "bold"), bg=THEMES[self.theme]['bg'], fg=THEMES[self.theme]['accent']).pack(pady=24)
        tk.Label(self.main_area, text=f"Files loaded: {len(self.file_list)}", font=("Segoe UI", 14), bg=THEMES[self.theme]['bg'], fg=THEMES[self.theme]['fg']).pack(pady=12)
        if self.file_list:
            for f in self.file_list[-5:]:
                tk.Label(self.main_area, text=os.path.basename(f), bg=THEMES[self.theme]['bg'], fg="#888").pack(anchor="w", padx=40)
        ttk.Button(self.main_area, text="Switch Theme", command=self.switch_theme).pack(pady=30)

    def show_encrypt(self):
        self.clear_main()
        t = THEMES[self.theme]
        tk.Label(self.main_area, text="Encrypt Files", font=("Segoe UI", 20, "bold"), bg=t['bg'], fg=t['accent']).pack(pady=16)
        file_frame = tk.Frame(self.main_area, bg=t['bg'])
        file_frame.pack(pady=10)
        ttk.Button(file_frame, text="Add Files", command=self.add_files).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Clear", command=self.clear_files).grid(row=0, column=1, padx=5)
        self.files_box = tk.Listbox(self.main_area, width=72, font=("Consolas", 10))
        self.files_box.pack(pady=8)
        self.update_files_box()
        # Encryption options
        optf = tk.Frame(self.main_area, bg=t['bg'])
        optf.pack(pady=7)
        tk.Label(optf, text="Encryption:", font=("Segoe UI",12), bg=t['bg'], fg=t['fg']).grid(row=0,column=0,sticky="e")
        self.method_var = tk.StringVar(value=self.encryption_method)
        vals = ["AES"] if AES_AVAILABLE else []
        vals.append("XOR")
        ttk.Combobox(optf, textvariable=self.method_var, values=vals, width=6, state="readonly").grid(row=0,column=1,padx=5)
        ttk.Button(self.main_area, text="Encrypt Selected", command=self.encrypt_selected).pack(pady=11)
        tk.Label(self.main_area, text="Tip: Drag-and-drop files here.", bg=t['bg'], fg="#888", font=("Segoe UI",9,"italic")).pack()

    def show_settings(self):
        self.clear_main()
        t = THEMES[self.theme]
        tk.Label(self.main_area, text="Settings", font=("Segoe UI", 20, "bold"), bg=t['bg'], fg=t['accent']).pack(pady=16)
        # Theme
        theme_frame = tk.Frame(self.main_area, bg=t['bg'])
        theme_frame.pack(pady=7)
        tk.Label(theme_frame, text="Theme:", font=("Segoe UI",12), bg=t['bg'], fg=t['fg']).grid(row=0,column=0,sticky="e",pady=6)
        theme_var = tk.StringVar(value=self.theme)
        cb = ttk.Combobox(theme_frame, textvariable=theme_var, values=["dark","light"], width=8, state="readonly")
        cb.grid(row=0,column=1,padx=5)
        def save_theme(*_):
            self.theme = theme_var.get()
            self.apply_theme()
            self.settings['theme'] = self.theme
            save_settings(self.settings)
        cb.bind("<<ComboboxSelected>>", save_theme)
        # Encryption
        enc_frame = tk.Frame(self.main_area, bg=t['bg'])
        enc_frame.pack(pady=7)
        tk.Label(enc_frame, text="Default Encryption:", font=("Segoe UI",12), bg=t['bg'], fg=t['fg']).grid(row=0,column=0,sticky="e",pady=6)
        enc_var = tk.StringVar(value=self.encryption_method)
        enc_vals = ["AES"] if AES_AVAILABLE else []
        enc_vals.append("XOR")
        enc_cb = ttk.Combobox(enc_frame, textvariable=enc_var, values=enc_vals, width=8, state="readonly")
        enc_cb.grid(row=0,column=1,padx=5)
        def save_enc(*_):
            self.encryption_method = enc_var.get()
            self.settings['encryption'] = self.encryption_method
            save_settings(self.settings)
        enc_cb.bind("<<ComboboxSelected>>", save_enc)

    # --- File Management ---
    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files to encrypt")
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
        self.update_files_box()

    def clear_files(self):
        self.file_list = []
        self.update_files_box()

    def update_files_box(self):
        if hasattr(self, 'files_box'):
            self.files_box.delete(0, tk.END)
            for f in self.file_list:
                self.files_box.insert(tk.END, f)

    # --- Encryption Actions ---
    def encrypt_selected(self):
        if not self.file_list:
            messagebox.showwarning("No files", "Please add files to encrypt.")
            return
        method = self.method_var.get()
        password = None
        if method == "AES":
            password = simpledialog.askstring("Password", "Enter password for AES encryption:", show="*")
            if not password:
                messagebox.showerror("No password", "Password required for AES encryption!")
                return
        output_dir = filedialog.askdirectory(title="Select output folder")
        if not output_dir:
            return

        def work():
            for i, f in enumerate(self.file_list):
                try:
                    with open(f, "rb") as infile:
                        data = infile.read()
                    if method == "AES":
                        enc = aes_encrypt(data, password)
                        outname = os.path.basename(f) + ".aes"
                    else:
                        enc = xor_encrypt(data)
                        outname = os.path.basename(f) + ".xor"
                    outpath = os.path.join(output_dir, outname)
                    with open(outpath, "wb") as outf:
                        outf.write(enc)
                except Exception as e:
                    self.notify(f"Error encrypting {os.path.basename(f)}: {str(e)}")
            self.notify("Encryption complete!")
            messagebox.showinfo("Done", "Encryption complete!")
        Thread(target=work).start()

    # --- Drag and Drop handler ---
    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if os.path.isfile(f):
                self.file_list.append(f)
        self.update_files_box()
        self.notify(f"{len(files)} file(s) added (drag & drop)")

    # --- Notification (status bar or pop up) ---
    def notify(self, msg):
        self.root.after(1, lambda: self.root.title(f"Ultimate Crypter 2025 - {msg}"))

    # --- Run App ---
    def run(self):
        self.root.mainloop()

# --- Entry Point ---
if __name__ == "__main__":
    try:
        app = UltimateCrypterApp()
        app.run()
    except Exception:
        tb = traceback.format_exc()
        with open("crypter_error.log", "w") as f:
            f.write(tb)
        print("Error! See crypter_error.log")