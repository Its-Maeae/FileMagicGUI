import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from converters import audio, video, image, pdf

class FileMagicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Magic")
        self.root.geometry("800x600")
        self.root.minsize(640, 480)
        self.root.resizable(True, True)

        self.file_data = {
            "audio": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
            "video": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
            "image": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
            "pdf": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
        }
        self.target_formats = {
            "audio": tb.StringVar(),
            "video": tb.StringVar(),
            "image": tb.StringVar()
        }
        self.file_display_frames = {}

        # Tabs
        self.tabs = tb.Notebook(root, bootstyle="dark")
        self.tabs.pack(padx=20, pady=20, expand=True, fill="both")

        self.setup_audio_tab()
        self.setup_video_tab()
        self.setup_image_tab()
        self.setup_pdf_tab()

        tb.Label(root, text="File Magic © 2025", bootstyle="secondary", font=("Helvetica Neue", 10)).pack(pady=5)

    def setup_tab_common(self, tab, formats, category):
        frame = ttk.Frame(tab)
        frame.pack(pady=10)

        tb.Button(frame, text="Dateien auswählen", bootstyle="danger-outline rounded",
                  command=lambda: self.select_files(category)).grid(row=0, column=0, padx=5)

        ttk.Label(frame, text="Zielformat:", background="#2b2b2b", foreground="#fff").grid(row=0, column=1, padx=5)

        format_menu = tb.Combobox(frame, textvariable=self.target_formats[category],
                                  values=list(formats), state="readonly", bootstyle="danger")
        format_menu.grid(row=0, column=2, padx=5)
        if formats:
            self.target_formats[category].set(formats[0])

        ttk.Label(frame, textvariable=self.file_data[category]["label_var"],
                  background="#2b2b2b", foreground="#fff").grid(row=1, column=0, columnspan=3, pady=5)

        display_frame = ttk.Frame(tab, style="Dark.TFrame")
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.file_display_frames[category] = display_frame

        # Drag & Drop
        display_frame.drop_target_register(DND_FILES)
        display_frame.dnd_bind('<<Drop>>', lambda e, c=category: self.handle_drop(e, c))

        return frame

    def setup_audio_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🎧 Audio")
        frame = self.setup_tab_common(tab, audio.ALLOWED_OUTPUTS, "audio")
        tb.Button(frame, text="Konvertieren", bootstyle="danger", command=self.convert_audio).grid(row=2, column=0, columnspan=3, pady=10)
        self.update_file_list_display("audio")

    def setup_video_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🎬 Video")
        frame = self.setup_tab_common(tab, video.ALLOWED_OUTPUTS, "video")
        tb.Button(frame, text="Konvertieren", bootstyle="danger", command=self.convert_video).grid(row=2, column=0, columnspan=3, pady=10)
        self.update_file_list_display("video")

    def setup_image_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🖼️ Bild")
        frame = self.setup_tab_common(tab, image.ALLOWED_OUTPUTS, "image")
        tb.Button(frame, text="Konvertieren", bootstyle="danger", command=self.convert_image).grid(row=2, column=0, columnspan=3, pady=10)
        self.update_file_list_display("image")

    def setup_pdf_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="📄 PDF")

        frame = ttk.Frame(tab)
        frame.pack(pady=10)

        ttk.Label(frame, textvariable=self.file_data["pdf"]["label_var"],
                  background="#2b2b2b", foreground="#fff").pack()

        tb.Button(frame, text="PDF splitten", bootstyle="danger", command=self.convert_pdf_split).pack(pady=5)
        tb.Button(frame, text="PDF zusammenfügen", bootstyle="danger", command=self.convert_pdf_merge).pack()

        display_frame = ttk.Frame(tab, style="Dark.TFrame")
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.file_display_frames["pdf"] = display_frame

        # Drag & Drop
        display_frame.drop_target_register(DND_FILES)
        display_frame.dnd_bind('<<Drop>>', lambda e, c="pdf": self.handle_drop(e, c))
        self.update_file_list_display("pdf")

    def select_files(self, category):
        new_files = filedialog.askopenfilenames()
        if new_files:
            self.file_data[category]["files"] = list(new_files)
            self.update_file_list_display(category)
            count = len(new_files)
            self.file_data[category]["label_var"].set(f"{count} Datei{'en' if count > 1 else ''} ausgewählt")
        else:
            self.file_data[category]["files"] = []
            self.update_file_list_display(category)
            self.file_data[category]["label_var"].set("Keine Dateien ausgewählt")

    def handle_drop(self, event, category):
        files = self.root.tk.splitlist(event.data)
        existing = self.file_data[category]["files"]
        new = [f for f in files if os.path.isfile(f) and f not in existing]
        if new:
            self.file_data[category]["files"].extend(new)
            self.update_file_list_display(category)
            count = len(self.file_data[category]["files"])
            self.file_data[category]["label_var"].set(f"{count} Datei{'en' if count > 1 else ''} ausgewählt")

    def update_file_list_display(self, category):
        display_frame = self.file_display_frames[category]
        for widget in display_frame.winfo_children():
            widget.destroy()

        files = self.file_data[category]["files"]
        if not files:
            # Drag & Drop Info anzeigen
            hint_label = ttk.Label(
                display_frame,
                text="📂 Dateien hierher ziehen",
                anchor="center",
                background="#2b2b2b",
                foreground="#999999",
                font=("Helvetica Neue", 12, "italic"),
                justify="center"
            )
            hint_label.place(relx=0.5, rely=0.5, anchor="center")
            return

        for filepath in files:
            filename = os.path.basename(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB"

            row = ttk.Frame(display_frame, style="Dark.TFrame")
            row.pack(fill="x", pady=2, padx=5)

            label = ttk.Label(row, text=f"{filename} ({size_str})", anchor="w",
                            background="#3c3f41", foreground="white", padding=5)
            label.pack(side="left", fill="x", expand=True)

            tk.Button(row, text="❌", fg="red", bg="#3c3f41", borderwidth=0,
                    activebackground="#3c3f41",
                    command=lambda f=filepath, c=category: self.remove_file(f, c)).pack(side="right")


    def remove_file(self, filepath, category):
        if filepath in self.file_data[category]["files"]:
            self.file_data[category]["files"].remove(filepath)
            self.update_file_list_display(category)
            count = len(self.file_data[category]["files"])
            self.file_data[category]["label_var"].set(
                "Keine Dateien ausgewählt" if count == 0 else f"{count} Datei{'en' if count > 1 else ''} ausgewählt"
            )

    def run_conversion(self, convert_func, category):
        files = self.file_data[category]["files"]
        target_var = self.target_formats.get(category)
        if files and target_var and target_var.get():
            try:
                convert_func(files, target_var.get())
                messagebox.showinfo("Fertig", "Dateien wurden erfolgreich konvertiert.")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
        else:
            messagebox.showwarning("Fehler", "Bitte wähle Dateien und ein Zielformat aus.")

    def convert_audio(self):
        self.run_conversion(audio.convert, "audio")

    def convert_video(self):
        self.run_conversion(video.convert, "video")

    def convert_image(self):
        self.run_conversion(image.convert, "image")

    def convert_pdf_split(self):
        self.files = self.file_data["pdf"]["files"]
        if self.files:
            try:
                pdf.split_pdfs(self.files)
                messagebox.showinfo("Fertig", "PDF wurde aufgeteilt.")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
        else:
            messagebox.showwarning("Fehler", "Bitte PDF-Dateien auswählen.")

    def convert_pdf_merge(self):
        self.files = self.file_data["pdf"]["files"]
        if self.files:
            try:
                pdf.merge_pdfs(self.files)
                messagebox.showinfo("Fertig", "PDF wurde zusammengeführt.")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
        else:
            messagebox.showwarning("Fehler", "Bitte PDF-Dateien auswählen.")


if __name__ == "__main__":
    app = TkinterDnD.Tk()
    style = tb.Style("superhero")  # Dark theme with red accents
    app.iconbitmap("appicon.ico")
    FileMagicApp(app)
    app.mainloop()
