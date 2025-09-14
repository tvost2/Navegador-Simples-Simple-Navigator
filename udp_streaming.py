from pathlib import Path
import time

CACHE_DIR = Path("./video_cache")
CACHE_DIR.mkdir(exist_ok=True)

def baixar_video_udp(url):
    filename = CACHE_DIR / f"{url.replace('/', '_')}.mp4"
    if filename.exists():
        print(f"♻️ Carregando do cache: {filename}")
        return filename
    print(f"⬇️ Baixando vídeo UDP: {url}")
    time.sleep(1)
    filename.write_text(f"Simulated video content from {url}")
    return filename
