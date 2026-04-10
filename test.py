from core.downloader import VideoDownloader

vdl = VideoDownloader(browser="firefox")

def download():
    url = input("Video link: ")
    try:
        vdl.download(url=url)
    except Exception as e:
        print(f"Error occured: {e}")
        print('''
            Known fixes:
              1. Make sure you are logged in
              2. Browser cookies are accessed
              3. Close all tabs in your browser and wait 15-30 minutes (if too many requests)
              4. Try another browser
              5. Try again later
''')

download()