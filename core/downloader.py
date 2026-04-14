from yt_dlp import YoutubeDL
from pathlib import Path
from tqdm import tqdm

from core.utils.url_validator import is_url

class VideoDownloader:
    def __init__(self, output_path: str = "downloads", browser: str | None = None, quality: str = "best"):
        self.output_path = output_path
        self.quality = quality
        self.pbar = None
        self.ydl_options = {
            "output_template": f"{output_path}/%(title)s.%(ext)s",
            "quiet": True,
            "format": self._get_format(quality),
            "remote_components": ["ejs:github"],
            "no_check_certificate": True,
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
        
        if browser is None:
            raise ValueError("Please provide your browser (-b chrome/firefox/etc.)")
        if browser.lower() in self.allowed_browsers:
            self.ydl_options["cookies_from_browser"] = browser
        else:
            raise ValueError("Browser is not allowed")
        
    def _get_format(self, quality: str) -> str:
        formats = {
            "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
            "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
            "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
            "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
            "audio": "bestaudio/best",
        }
        return formats.get(quality.lower(), formats["best"])
    
    def _map_audio_quality(self, quality: str) -> str:
        """yt-dlp audioquality: 0 (best) - 9 (worst)"""
        mapping = {
            "best": "0",
            "1080p": "2",
            "720p": "3",
            "480p": "5",
            "360p": "7",
            "audio": "0",
        }
        return mapping.get(quality.lower(), "0")

    def _map_audio_bitrate(self, quality: str) -> str:
        """Битрейт в kbps для MP3"""
        mapping = {
            "best": "320",
            "1080p": "256",
            "720p": "192",
            "480p": "128",
            "360p": "96",
            "audio": "320",
        }
        return mapping.get(quality.lower(), "192")

    def download(self, url: str, audio_only: bool = False) -> dict:
        self.ydl_options["progress_hooks"] = [self._progress_hook]
        if not is_url(url):
            return None

        if audio_only:
            audio_options = {
                "extract_audio": True,
                "audioformat": "mp3",
                "audioquality": self._map_audio_quality(self.quality),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": self._map_audio_bitrate(self.quality)
                }]
            }
            self.ydl_options.update(audio_options)

        with YoutubeDL(self.ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)
            return info
    
    @staticmethod
    def get_info(url: str) -> dict:
        if not is_url(url):
            return None
        
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
            else:
                # Обновляем: downloaded - self.pbar.n = сколько скачалось с последнего раза
                self.pbar.update(downloaded - self.pbar.n)
            
        elif d["status"] == "finished":
            # Загрузка завершена — закрываем бар
            if self.pbar:
                self.pbar.close()
                self.pbar = None