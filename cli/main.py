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
    def do_download(self, arg):
        """Download video. Example: download <url> [options]"""
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


if __name__ == "__main__":
    SinGrabberShell().cmdloop()