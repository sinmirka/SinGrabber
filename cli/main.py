import cmd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.downloader import VideoDownloader

class SinGrabberShell(cmd.Cmd):
    intro = """
░██████╗██╗███╗░░██╗  ░██████╗░██████╗░░█████╗░██████╗░██████╗░███████╗██████╗░  ░█████╗░██╗░░░░░██╗
██╔════╝██║████╗░██║  ██╔════╝░██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗  ██╔══██╗██║░░░░░██║
╚█████╗░██║██╔██╗██║  ██║░░██╗░██████╔╝███████║██████╦╝██████╦╝█████╗░░██████╔╝  ██║░░╚═╝██║░░░░░██║
░╚═══██╗██║██║╚████║  ██║░░╚██╗██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝░░██╔══██╗  ██║░░██╗██║░░░░░██║
██████╔╝██║██║░╚███║  ╚██████╔╝██║░░██║██║░░██║██████╦╝██████╦╝███████╗██║░░██║  ╚█████╔╝███████╗██║
╚═════╝░╚═╝╚═╝░░╚══╝  ░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝  ░╚════╝░╚══════╝╚═╝
Welcome to SinGrabber CLI
Type "help" or "?" help
    """

    prompt = "singrabber> "

    def parse_args(self, arg) -> str: # returns url, output, browser
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
        url, output, browser = self.parse_args(arg=arg)

        try:
            print(f"Downloading: {url}")
            downloader = VideoDownloader(output_path=output, browser=browser)
            info = downloader.download(url=url)
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
        url, output, browser = self.parse_args(arg=arg)

        try:
            print(f"Extracting info from {url}")
            downloader = VideoDownloader(output_path=output, browser=browser)
            info = downloader.get_info(url=url)
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