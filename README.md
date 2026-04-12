# SinGrabber

CLI tool for downloading videos and audio from YouTube and other platforms. Built on top of `yt-dlp`.

> ⚠️ **Learning project.** This is not production-ready software. Made for educational purposes — learning Python, CLI design, and working with media download libraries.

## Features

- 🎬 Download videos from 1000+ sites (powered by yt-dlp)
- 🎵 Extract audio as MP3
- 📋 View video metadata without downloading
- 📊 Real-time download progress bar
- 🔐 Browser cookie authentication (YouTube, etc.)
- 🎨 Clean interactive CLI

## Prerequisites

### System dependencies

These must be installed on your system:

| Tool   | Why                    | Install                           |
|--------|------------------------|-----------------------------------|
| FFmpeg | Audio extraction       | `winget install Gyan.FFmpeg`      |
| Deno   | YouTube JS runtime     | `winget install DenoLand.Deno`    |

After installation, **restart your terminal** so PATH updates.

Verify:
```bash
ffmpeg -version
deno --version
```

### Python dependencies

```bash
pip install -r requirements.txt
```

## Quick start

```bash
# Run the CLI
python main.py
```

You'll enter an interactive shell. Available commands:

### `download <url> [options]`

Download a video:
```
singrabber> download https://youtube.com/watch?v=VIDEO_ID
singrabber> download <url> -o ./my_folder
singrabber> download <url> -b firefox
```

Options:
- `-o, --output <path>` — custom output directory (default: `downloads`)
- `-b, --browser <name>` — browser for cookie extraction (`chrome`, `firefox`, `edge`, etc.)

### `audio <url> [options]`

Extract and download audio as MP3:
```
singrabber> audio https://youtube.com/watch?v=VIDEO_ID
singrabber> audio <url> -b firefox
```

Same options as `download`.

### `info <url> [options]`

View video metadata without downloading:
```
singrabber> info https://youtube.com/watch?v=VIDEO_ID
```

Shows: title, author, duration, views, description.

### `exit` / `Ctrl+D`

Quit the CLI.

## Project structure

```
SinGrabber/
├── main.py              # Entry point
├── cli/
│   ├── __init__.py
│   ├── main.py          # CLI shell (cmd.Cmd)
│   └── intro.py         # Gradient banner
├── core/
│   ├── __init__.py
│   └── downloader.py    # yt-dlp wrapper
└── requirements.txt
```

## How it works

1. **CLI** — built on Python's built-in `cmd` module for interactive shell
2. **Downloads** — wraps `yt-dlp` with custom options and progress hooks
3. **Progress bar** — `tqdm` + yt-dlp's `progress_hooks` callback system
4. **Authentication** — reads cookies directly from your browser via yt-dlp
5. **Audio extraction** — FFmpeg post-processor via yt-dlp's `postprocessors`

## Development

```bash
# Activate venv
.venv/Scripts/activate

# Install deps
pip install -r requirements.txt

# Run
python main.py
```

## Tech stack

- **Python 3.13+**
- **yt-dlp** — media downloading engine
- **tqdm** — progress bars
- **colorama** — terminal colors (Windows-compatible)
- **Pillow** — color utilities (gradient)

## License

MIT. See [LICENSE](LICENSE) for details.
