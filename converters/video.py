import os, subprocess

ALLOWED_OUTPUTS = ['mp4', 'avi', 'mkv', 'webm', 'mov']

def convert(files, target_format):
    os.makedirs("output", exist_ok=True)
    for file in files:
        base = os.path.splitext(os.path.basename(file))[0].replace(" ", "_")
        out_path = os.path.join("output", f"{base}.{target_format}")
        result = subprocess.run([
            "libs/ffmpeg.exe", "-i", file,
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k", out_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Video-Konvertierung fehlgeschlagen für '{base}':\n{result.stderr}")


        
        