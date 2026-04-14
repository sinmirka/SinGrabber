import cmd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from colorama import init, Style
init()

from core.downloader import VideoDownloader
from cli.intro import gradient_intro

class SinGrabberShell(cmd.Cmd):
    intro = gradient_intro

    prompt_color = (252, 92, 125)
    prompt = f"\033[38;2;{prompt_color[0]};{prompt_color[1]};{prompt_color[2]}msingrabber> " + Style.RESET_ALL

    def _handle_args(self, arg):
        args = self.parse_args(arg=arg)
        if args is None:
            return None
        return args
    
    def parse_args(self, arg) -> dict: # returns url, output, browser
        if arg is None:
            return
        parts = arg.split()
        if not parts:
            print("Error: provide URL")
            return

        url = parts[0]
        output = "downloads"
        browser = None
        quality = "best"

        # parsing args
        i = 1
        while i < len(parts):
            if parts[i] in ("-o", "--output") and i + 1 < len(parts):
                output = parts[i + 1]
                i += 2
            elif parts[i] in ("-b", "--browser") and i + 1 < len(parts):
                browser = parts[i + 1]
                i += 2
            elif parts[i] in ("-q", "--quality") and i + 1 < len(parts):
                quality = parts[i + 1]
                i += 2
            else:
                i += 1
        
        return {
            "url": url,
            "output": output,
            "browser": browser,
            "quality": quality,
        }

    def do_download(self, arg):
        """Download video. Example: download <url> [-b browser] [-q quality] [-o output]"""
        args = self._handle_args(arg=arg)

        try:
            print(f"Downloading: {args.get('url', 'Unknown')}")
            downloader = VideoDownloader(
                output_path=args['output'],
                browser=args['browser'],
                quality=args['quality'],
            )
            info = downloader.download(url=args['url'], audio_only=False)
            print(f"Done: {info.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error: {e}")

    def do_audio(self, arg):
        """Download audio. Example: audio <url> [options]"""
        args = self._handle_args(arg=arg)

        try:
            print(f"Downloading audio from {args.get('url', 'Unknown')}")
            downloader = VideoDownloader(
                output_path=args['output'],
                browser=args['browser'],
                quality=args['quality'],
            )
            info = downloader.download(url=args['url'], audio_only=True)
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
        args = self._handle_args(arg=arg)

        try:
            print(f"Extracting info from {args.get('url', 'Unknown')}")
            info = VideoDownloader.get_info(url=args['url'])
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