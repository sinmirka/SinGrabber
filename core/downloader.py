from yt_dlp import YoutubeDL
from pathlib import Path
from tqdm import tqdm
import re

def is_url(url):
    pattern = r'^https://[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}'
    if not re.match(pattern, url):
        print("URL is invalid: URL must start with 'https://' and contain valid domain")
        return False
    return True

class VideoDownloader:
    def __init__(self, output_path: str = "downloads", browser: str | None = None):
        self.output_path = output_path
        self.pbar = None
        self.ydl_options = {
            "output_template": f"{output_path}/%(title)s.%(ext)s",
            "quiet": True,
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        }
        self.allowed_browsers = [
            'chrome',
            'firefox',
            'edge',
            'opera',
            'brave',
            'vivaldi',
            'safari'
        ]
        
        if browser == None:
            raise ValueError("Please provide your browser (-b chrome/firefox/etc.)")
        if browser.lower() in self.allowed_browsers:
            self.ydl_options["cookies_from_browser"] = browser
        else:
            raise ValueError("Browser is not allowed")

    def download(self, url: str, audio_only: bool | None) -> dict:
        self.ydl_options["progress_hooks"] = [self._progress_hook]
        self.ydl_options["remote_components"] = ["ejs:github"]
        self.ydl_options["no_check_certificate"] = True
        if not is_url(url):
            return

        if audio_only:
            audio_options = {
                "extract_audio": True,
                "audioformat": "mp3",
                "audioquality": "9",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]
            }
            self.ydl_options.update(audio_options)

        with YoutubeDL(self.ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)
            return info
    
    def get_info(url: str) -> dict:
        if not is_url(url):
            return
        
        ydl_options = {
            "quiet": True
        }
        with YoutubeDL(ydl_options) as ydl:
            return ydl.extract_info(url=url, download=False)
    
    def _progress_hook(self, d):
        # yt-dlp вызывает эту функцию при каждом обновлении загрузки
        # d — это словарь с данными о прогрессе
        
        if d["status"] == "downloading":
            # total_bytes или total_bytes_estimate — размер файла
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            
            # Если прогресс-бар ещё не создан — создаём
            if self.pbar is None:
                self.pbar = tqdm(
                    total=total,
                    unit="B",
                    unit_scale=True,  # чтобы было 1.5MB, а не 1500000
                    unit_divisor=1024,
                    desc="Downloading",
                    colour="green"
                )
            
            # Обновляем: downloaded - self.pbar.n = сколько скачалось с последнего раза
            self.pbar.update(downloaded - self.pbar.n)
            
        elif d["status"] == "finished":
            # Загрузка завершена — закрываем бар
            if self.pbar:
                self.pbar.close()
                self.pbar = None