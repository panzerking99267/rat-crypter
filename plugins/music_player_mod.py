def register(app):
    import threading
    from tkinter import filedialog, messagebox
    def play_music():
        file = filedialog.askopenfilename(title="Select music file", filetypes=[("Music files", "*.mp3 *.wav")])
        if not file:
            return
        try:
            # Try to use pygame for cross-platform audio
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            messagebox.showinfo("Music Player", "Now playing!\n\nClose this dialog to stop music.")
            pygame.mixer.music.stop()
        except ImportError:
            try:
                import winsound
                winsound.PlaySound(file, winsound.SND_FILENAME)
            except Exception:
                messagebox.showerror("Music Player", "Install pygame (pip install pygame) or use a .wav file on Windows!")
        except Exception as e:
            messagebox.showerror("Music Player", str(e))
    app.add_tools_menu("🎵 Play Music", lambda: threading.Thread(target=play_music).start())