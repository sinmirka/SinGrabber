# SinGrabber

CLI utility for downloading video and audio from YouTube and other platforms. Wrapper around `yt-dlp` with an interactive shell.

> **Pet project.** Not production-ready. Built for educational purposes — learning Python, CLI design, and media downloading.

## Features

- Video download from 1000+ sites (yt-dlp)
- Audio extraction to MP3
- View metadata without downloading
- Real-time progress bar
- Browser cookie authentication
- Interactive CLI shell

## Requirements

### System dependencies

| Tool   | Purpose                  | Installation                     |
|--------|--------------------------|----------------------------------|
| FFmpeg | Audio extraction/conversion | `winget install Gyan.FFmpeg`  |
| Deno   | YouTube JS runtime       | `winget install DenoLand.Deno`   |

Restart your terminal after installation.

Verify:
```bash
ffmpeg -version
deno --version
```

### Python dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

You'll enter an interactive shell. Available commands:

### `download <url> [options]`

```
singrabber> download https://youtube.com/watch?v=VIDEO_ID
singrabber> download <url> -o ./my_folder
singrabber> download <url> -b firefox
```

Options:
- `-o, --output <path>` — output directory (default: `downloads`)
- `-b, --browser <name>` — browser for cookie extraction (`chrome`, `firefox`, `edge`, `brave`, `opera`, `vivaldi`, `safari`)

### `audio <url> [options]`

Download audio as MP3 (192 kbps):
```
singrabber> audio https://youtube.com/watch?v=VIDEO_ID
```

### `info <url> [options]`

Metadata without downloading:
```
singrabber> info https://youtube.com/watch?v=VIDEO_ID
```

Output: title, author, duration, views, description.

### `exit` / `Ctrl+D`

Exit the CLI.

## Project structure

```
SinGrabber/
├── main.py              # Entry point
├── cli/
│   ├── main.py          # CLI shell (cmd.Cmd)
│   └── intro.py         # Gradient banner
├── core/
│   └── downloader.py    # yt-dlp wrapper
└── requirements.txt
```

## Architecture

- **CLI** — Python's built-in `cmd` module
- **Downloads** — custom yt-dlp options + progress hooks
- **Progress** — `tqdm` via `progress_hooks` callback
- **Authentication** — reads cookies directly from browser
- **Audio** — FFmpeg post-processor through yt-dlp

## Roadmap

- [ ] Telegram bot integration
- [ ] Batch downloading (playlists, URL lists)
- [ ] Config file for default options
- [ ] Quality presets

## Development

```bash
# Activate venv
.venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## Stack

- **Python 3.13+**
- **yt-dlp** — download engine
- **tqdm** — progress bars
- **colorama** — terminal colors (Windows)
- **Pillow** — gradient utilities

## License

MIT. See [LICENSE](LICENSE).
