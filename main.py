import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from converters import audio, video, image, pdf

class FileMagicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Magic – Konverter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.files = []
        self.target_format = tk.StringVar()

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both")

        self.setup_audio_tab()
        self.setup_video_tab()
        self.setup_image_tab()
        self.setup_pdf_tab()

    def setup_tab_common(self, tab, formats):
        frame = ttk.Frame(tab)
        frame.pack(pady=10)

        btn_select = ttk.Button(frame, text="Dateien auswählen", command=self.select_files)
        btn_select.grid(row=0, column=0, padx=5)

        ttk.Label(frame, text="Zielformat:").grid(row=0, column=1, padx=5)
        format_menu = ttk.Combobox(frame, textvariable=self.target_format, values=list(formats), state="readonly")
        format_menu.grid(row=0, column=2, padx=5)
        format_menu.current(0)

        return frame

    def setup_audio_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🎧 Audio")
        frame = self.setup_tab_common(tab, audio.ALLOWED_OUTPUTS)
        ttk.Button(frame, text="Konvertieren", command=self.convert_audio).grid(row=1, column=0, columnspan=3, pady=10)

    def setup_video_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🎬 Video")
        frame = self.setup_tab_common(tab, video.ALLOWED_OUTPUTS)
        ttk.Button(frame, text="Konvertieren", command=self.convert_video).grid(row=1, column=0, columnspan=3, pady=10)

    def setup_image_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="🖼️ Bild")
        frame = self.setup_tab_common(tab, image.ALLOWED_OUTPUTS)
        ttk.Button(frame, text="Konvertieren", command=self.convert_image).grid(row=1, column=0, columnspan=3, pady=10)

    def setup_pdf_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="📄 PDF")
        frame = ttk.Frame(tab)
        frame.pack(pady=20)
        ttk.Button(frame, text="PDF splitten", command=self.convert_pdf_split).pack(pady=5)
        ttk.Button(frame, text="PDF zusammenfügen", command=self.convert_pdf_merge).pack()

    def select_files(self):
        self.files = filedialog.askopenfilenames()
        if self.files:
            messagebox.showinfo("Dateien ausgewählt", f"{len(self.files)} Datei(en) gewählt.")

    def convert_audio(self):
        if self.files:
            audio.convert(self.files, self.target_format.get())
            messagebox.showinfo("Fertig", "Audio-Dateien wurden konvertiert.")
        else:
            messagebox.showwarning("Fehler", "Bitte wähle Dateien aus.")

    def convert_video(self):
        if self.files:
            video.convert(self.files, self.target_format.get())
            messagebox.showinfo("Fertig", "Video-Dateien wurden konvertiert.")
        else:
            messagebox.showwarning("Fehler", "Bitte wähle Dateien aus.")

    def convert_image(self):
        if self.files:
            image.convert(self.files, self.target_format.get())
            messagebox.showinfo("Fertig", "Bild-Dateien wurden konvertiert.")
        else:
            messagebox.showwarning("Fehler", "Bitte wähle Dateien aus.")

    def convert_pdf_split(self):
        self.files = filedialog.askopenfilenames(filetypes=[("PDF-Dateien", "*.pdf")])
        if self.files:
            pdf.split_pdfs(self.files)
            messagebox.showinfo("Fertig", "PDF wurde aufgeteilt.")
        else:
            messagebox.showwarning("Fehler", "Bitte PDF-Datei auswählen.")

    def convert_pdf_merge(self):
        self.files = filedialog.askopenfilenames(filetypes=[("PDF-Dateien", "*.pdf")])
        if self.files:
            pdf.merge_pdfs(self.files)
            messagebox.showinfo("Fertig", "PDF wurde zusammengeführt.")
        else:
            messagebox.showwarning("Fehler", "Bitte PDF-Dateien auswählen.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMagicApp(root)
    root.mainloop()
