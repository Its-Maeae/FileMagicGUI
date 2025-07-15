import os, subprocess

ALLOWED_OUTPUTS = ['mp3', 'wav', 'ogg', 'flac', 'm4a']

def convert(files, target_format):
    os.makedirs("output", exist_ok=True)
    for file in files:
        base = os.path.splitext(os.path.basename(file))[0].replace(" ", "_")
        out_path = os.path.join("output", f"{base}.{target_format}")
        result = subprocess.run([
            "libs/ffmpeg.exe", "-i", file,
            "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", out_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Audio-Konvertierung fehlgeschlagen für '{base}':\n{result.stderr}")
