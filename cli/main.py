import cmd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from colorama import init, Fore, Style
init()

from core.downloader import VideoDownloader
from cli.intro import gradient_intro

class SinGrabberShell(cmd.Cmd):
    intro = gradient_intro

    prompt_color = (252, 92, 125)
    prompt = f"\033[38;2;{prompt_color[0]};{prompt_color[1]};{prompt_color[2]}msingrabber> " + Style.RESET_ALL

    def parse_args(self, arg) -> tuple: # returns url, output, browser
        if arg == None:
            return
        parts = arg.split()
        if not parts:
            print("Error: provide URL")
            return

        url = parts[0]
        output = "downloads"
        browser = None

        # parsing args
        i = 1
        while i < len(parts):
            if parts[i] in ("-o", "--output") and i + 1 < len(parts):
                output = parts[i + 1]
                i += 2
            elif parts[i] in ("-b", "--browser") and i + 1 < len(parts):
                browser = parts[i + 1]
                i += 2
            else:
                i += 1
        
        return url, output, browser

    def do_download(self, arg):
        """Download video. Example: download <url> [options]"""
        result = self.parse_args(arg=arg)
        if result is None:
            return
        url, output, browser = result

        try:
            print(f"Downloading: {url}")
            downloader = VideoDownloader(output_path=output, browser=browser)
            info = downloader.download(url=url, audio_only=False)
            print(f"Done: {info.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error: {e}")

    def do_audio(self, arg):
        """Download audio. Example: audio <url> [options]"""
        result = self.parse_args(arg=arg)
        if result is None:
            return
        url, output, browser = result

        try:
            print(f"Downloading audio from {url}")
            downloader = VideoDownloader(output_path=output, browser=browser)
            info = downloader.download(url=url, audio_only=True)
            print(f"Done: {info.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error: {e}")

    def do_exit(self, arg):
        """Exit CLI"""
        print("Closing")
        return True

    def do_EOF(self, arg):
        """Ctrl+D for exit."""
        return True

    def do_info(self, arg):
        """Parse video information. Example: info <url> [options]"""
        result = self.parse_args(arg=arg)
        if result is None:
            return
        url, output, browser = result

        try:
            print(f"Extracting info from {url}")
            info = VideoDownloader.get_info(url=url)
            print(f"Done extracting info")
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Author: {info.get('channel', 'Unknown')}")
            print(f"Duration: {info.get('duration', 'Unknown')} sec")
            print(f"Views: {info.get('view_count', 'Unknown')}")
            print(f"Description: {info.get('description', 'N/A')[:100]}...")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    SinGrabberShell().cmdloop()