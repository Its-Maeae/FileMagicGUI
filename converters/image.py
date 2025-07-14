import os
from PIL import Image

ALLOWED_OUTPUTS = ['png', 'jpg', 'webp', 'bmp']

def convert(files, target_format):
    os.makedirs("output", exist_ok=True)
    for file in files:
        base = os.path.splitext(os.path.basename(file))[0]
        out_path = os.path.join("output", f"{base}.{target_format}")
        with Image.open(file) as img:
            img.convert("RGB").save(out_path, format=target_format.upper())