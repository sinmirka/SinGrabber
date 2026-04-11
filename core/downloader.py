from yt_dlp import YoutubeDL
from pathlib import Path

class VideoDownloader:
    def __init__(self, output_path: str = "downloads", browser: str | None = None):
        self.output_path = output_path
        self.ydl_options = {
            "output_template": f"{output_path}/%(title)s.%(ext)s",
            "quiet": False,
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
    
    def download(self, url: str) -> dict:
        with YoutubeDL(self.ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)
            return info
    
    def get_info(self, url: str) -> dict:
        with YoutubeDL(self.ydl_options) as ydl:
            info = ydl.extract_info(url=url, download=False)
            return info