import os
from PIL import Image

ALLOWED_OUTPUTS = ['png', 'jpg', 'webp', 'bmp']

def convert(files, target_format):
    os.makedirs("output", exist_ok=True)
    for file in files:
        base = os.path.splitext(os.path.basename(file))[0].replace(" ", "_")
        out_path = os.path.join("output", f"{base}.{target_format}")
        try:
            with Image.open(file) as img:
                img.convert("RGB").save(out_path, format=target_format.upper())
        except Exception as e:
            raise RuntimeError(f"Bild-Konvertierung fehlgeschlagen für '{base}':\n{str(e)}")
