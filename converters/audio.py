import os, subprocess, uuid
ALLOWED_OUTPUTS = ['mp3', 'wav', 'ogg', 'flac', 'm4a']

def convert(files, target_format):
    os.makedirs("output", exist_ok=True)
    for file in files:
        base = os.path.splitext(os.path.basename(file))[0]
        out_path = os.path.join("output", f"{base}.{target_format}")
        result = subprocess.run([
            "libs/ffmpeg.exe", "-i", file,
            "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", out_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[FFMPEG-Fehler] {result.stderr}")
        else:
            print(f"[Audio konvertiert] → {out_path}")