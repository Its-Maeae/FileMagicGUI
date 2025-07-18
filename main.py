import ttkbootstrap as tb
from ttkbootstrap.constants import *
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

    def setup_tab_common(self, tab, formats):
        frame = tb.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")

        tb.Button(frame, text="Dateien auswählen", bootstyle="outline", command=self.select_files).pack(pady=10)

        tb.Label(frame, text="Zielformat:", font=("Helvetica Neue", 12)).pack()
        tb.Combobox(frame, textvariable=self.target_format, values=list(formats),
                    state="readonly", bootstyle="light").pack(pady=5)

        tb.Label(frame, textvariable=self.file_label, font=("Helvetica Neue", 10), foreground="#888").pack(pady=10)

        return frame

    def setup_audio_tab(self):
        tab = tb.Frame(self.tabs)
        self.tabs.add(tab, text="🎧 Audio")
        frame = self.setup_tab_common(tab, audio.ALLOWED_OUTPUTS)
        tb.Button(frame, text="Konvertieren", bootstyle="success", command=self.convert_audio).pack(pady=10)

    def setup_video_tab(self):
        tab = tb.Frame(self.tabs)
        self.tabs.add(tab, text="🎬 Video")
        frame = self.setup_tab_common(tab, video.ALLOWED_OUTPUTS)
        tb.Button(frame, text="Konvertieren", bootstyle="success", command=self.convert_video).pack(pady=10)

    def setup_image_tab(self):
        tab = tb.Frame(self.tabs)
        self.tabs.add(tab, text="🖼️ Bild")
        frame = self.setup_tab_common(tab, image.ALLOWED_OUTPUTS)
        tb.Button(frame, text="Konvertieren", bootstyle="success", command=self.convert_image).pack(pady=10)

    def setup_pdf_tab(self):
        tab = tb.Frame(self.tabs)
        self.tabs.add(tab, text="📄 PDF")
        frame = tb.Frame(tab, padding=20)
        frame.pack(expand=True, fill="both")

        tb.Button(frame, text="PDF splitten", bootstyle="warning", command=self.convert_pdf_split).pack(pady=10)
        tb.Button(frame, text="PDF zusammenfügen", bootstyle="info", command=self.convert_pdf_merge).pack()

    def select_files(self):
        self.files = filedialog.askopenfilenames()
        count = len(self.files)
        if count == 0:
            self.file_label.set("Keine Dateien ausgewählt")
        elif count == 1:
            self.file_label.set("1 Datei ausgewählt")
        else:
            self.file_label.set(f"{count} Dateien ausgewählt")

    def run_conversion(self, convert_func):
        if self.files and self.target_format.get():
            for file in self.files:
                convert_func([file], self.target_format.get())
            messagebox.showinfo("Fertig", "Dateien wurden erfolgreich konvertiert.")
        else:
            messagebox.showwarning("Fehler", "Bitte wähle Dateien und ein Zielformat aus.")

    def convert_audio(self):
        self.run_conversion(audio.convert)

    def convert_video(self):
        self.run_conversion(video.convert)

    def convert_image(self):
        self.run_conversion(image.convert)

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
