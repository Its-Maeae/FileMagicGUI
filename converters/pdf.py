import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from converters import audio, video, image, pdf
from PyPDF2 import PdfReader, PdfWriter

def split_pdfs(files):
    os.makedirs("output", exist_ok=True)
    for file in files:
        reader = PdfReader(file)
        base = os.path.splitext(os.path.basename(file))[0].replace(" ", "_")
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            out_path = os.path.join("output", f"{base}_page{i+1}.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)

def merge_pdfs(files):
    os.makedirs("output", exist_ok=True)
    try:
        writer = PdfWriter()
        for file in files:
            reader = PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)
        out_path = os.path.join("output", "merged.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
    except Exception as e:
        raise RuntimeError(f"PDF-Merge fehlgeschlagen:\n{str(e)}")