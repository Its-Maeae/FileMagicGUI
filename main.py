import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import filedialog, messagebox
from converters import audio, video, image, pdf

class FileMagicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Magic")
        self.root.geometry("800x600")
        self.root.minsize(640, 480)
        self.root.resizable(True, True)
        self.root.configure(background="#f0f0f0")

        self.files = []
        self.target_format = tb.StringVar()
        self.file_label = tb.StringVar(value="Keine Dateien ausgewählt")
        self.file_data = {
            "audio": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
            "video": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
            "image": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
            "pdf": {"files": [], "label_var": tk.StringVar(value="Keine Dateien ausgewählt")},
        }
        self.file_display_frames = {}  # Dict für GUI-Anzeige pro Tab

        # Tabs
        self.tabs = tb.Notebook(root, bootstyle="secondary")
        self.tabs.pack(padx=20, pady=20, expand=True, fill="both")

        self.setup_audio_tab()
        self.setup_video_tab()
        self.setup_image_tab()
        self.setup_pdf_tab()

        # Footer
        self.footer = tb.Label(root, text="File Magic © 2025", bootstyle="secondary", font=("Helvetica Neue", 10))
        self.footer.pack(pady=5)

    def setup_tab_common(self, tab, formats, category):
        frame = ttk.Frame(tab)
        frame.pack(pady=10)

        btn_select = ttk.Button(frame, text="Dateien auswählen", command=lambda: self.select_files(category))
        btn_select.grid(row=0, column=0, padx=5)

        ttk.Label(frame, text="Zielformat:").grid(row=0, column=1, padx=5)
        format_menu = ttk.Combobox(frame, textvariable=self.target_format, values=list(formats), state="readonly")
        format_menu.grid(row=0, column=2, padx=5)
        format_menu.current(0)

        ttk.Label(frame, textvariable=self.file_data[category]["label_var"]).grid(row=1, column=0, columnspan=3, pady=5)

        display_frame = ttk.Frame(tab)
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.file_display_frames[category] = display_frame

        return frame

    def setup_audio_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🎧 Audio")
        frame = self.setup_tab_common(tab, audio.ALLOWED_OUTPUTS, "audio")
        ttk.Button(frame, text="Konvertieren", command=self.convert_audio).grid(row=2, column=0, columnspan=3, pady=10)

    def setup_video_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🎬 Video")
        frame = self.setup_tab_common(tab, video.ALLOWED_OUTPUTS, "video")
        ttk.Button(frame, text="Konvertieren", command=self.convert_video).grid(row=2, column=0, columnspan=3, pady=10)

    def setup_image_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🖼️ Bild")
        frame = self.setup_tab_common(tab, image.ALLOWED_OUTPUTS, "image")
        ttk.Button(frame, text="Konvertieren", command=self.convert_image).grid(row=2, column=0, columnspan=3, pady=10)

    def setup_pdf_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="📄 PDF")

        frame = ttk.Frame(tab)
        frame.pack(pady=10)

        label = ttk.Label(frame, textvariable=self.file_data["pdf"]["label_var"])
        label.pack()

        ttk.Button(frame, text="PDF splitten", command=self.convert_pdf_split).pack(pady=5)
        ttk.Button(frame, text="PDF zusammenfügen", command=self.convert_pdf_merge).pack()

        display_frame = ttk.Frame(tab)
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.file_display_frames["pdf"] = display_frame

    def select_files(self, category):
        new_files = filedialog.askopenfilenames()
        if new_files:
            self.file_data[category]["files"] = list(new_files)
            self.update_file_list_display(category)
            count = len(new_files)
            self.file_data[category]["label_var"].set(
                f"{count} Datei{'en' if count > 1 else ''} ausgewählt"
            )
        else:
            self.file_data[category]["files"] = []
            self.update_file_list_display(category)
            self.file_data[category]["label_var"].set("Keine Dateien ausgewählt")


    def update_file_list_display(self, category):
        display_frame = self.file_display_frames[category]
        for widget in display_frame.winfo_children():
            widget.destroy()

        for filepath in self.file_data[category]["files"]:
            filename = os.path.basename(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB"

            row = ttk.Frame(display_frame)
            row.pack(fill="x", pady=2)

            ttk.Label(row, text=f"{filename} ({size_str})", anchor="w").pack(side="left", expand=True, fill="x")

            tk.Button(row, text="❌", fg="red", borderwidth=0,
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
        format = self.target_format.get()

        if not files:
            messagebox.showwarning("Fehler", "Bitte Dateien auswählen.")
            return
        if not format:
            messagebox.showwarning("Fehler", "Bitte Zielformat auswählen.")
            return

        try:
            convert_func(files, format)
            messagebox.showinfo("Fertig", "Dateien wurden erfolgreich konvertiert.")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))


    def convert_audio(self):
        self.run_conversion(audio.convert, "audio")

    def convert_video(self):
        self.run_conversion(video.convert, "video")

    def convert_image(self):
        self.run_conversion(image.convert, "image")

    def convert_pdf_split(self):
        self.files = filedialog.askopenfilenames(filetypes=[("PDF-Dateien", "*.pdf")])
        if self.files:
            try:
                pdf.split_pdfs(self.files)
                messagebox.showinfo("Fertig", "PDF wurde aufgeteilt.")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))

    def convert_pdf_merge(self):
        self.files = filedialog.askopenfilenames(filetypes=[("PDF-Dateien", "*.pdf")])
        count = len(self.files)
        self.file_label.set(f"{count} PDF{'s' if count > 1 else ''} ausgewählt")
        if self.files:
            try:
                pdf.merge_pdfs(self.files)  # <-- Aufruf der Funktion im Modul pdf.py
                messagebox.showinfo("Fertig", "PDF wurde zusammengeführt.")
            except Exception as e:
                messagebox.showerror("Fehler", str(e))
        else:
            messagebox.showwarning("Fehler", "Bitte PDF-Dateien auswählen.")

if __name__ == "__main__":
    app = tb.Window(themename="flatly") 
    app.iconbitmap("appicon.ico") 
    FileMagicApp(app)
    app.mainloop()
