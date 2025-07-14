import os, subprocess
ALLOWED_OUTPUTS = ['mp4', 'avi', 'mkv', 'webm', 'mov']

def convert(files, target_format):
    os.makedirs("output", exist_ok=True)
    for file in files:
        base = os.path.splitext(os.path.basename(file))[0]
        out_path = os.path.join("output", f"{base}.{target_format}")
        result = subprocess.run([
            "libs/ffmpeg.exe", "-i", file,
            "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "192k",
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[FFMPEG-Fehler] {result.stderr}")
        else:
            print(f"[Audio konvertiert] → {out_path}")
        
        