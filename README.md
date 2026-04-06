# 🎬 Video Downloader

A simple but powerful command-line video downloader built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp). Download videos from YouTube, Instagram, TikTok, Twitter/X, Facebook, Vimeo, Dailymotion, and 1000+ other sites.

---

## ✨ Features

- 🎥 Downloads highest quality video + audio (with ffmpeg)
- 🎵 Audio-only extraction as MP3
- 📋 List all available formats before downloading
- 📁 Custom output directory
- 🔄 Graceful fallback when ffmpeg is not installed
- 🌐 Works with 1000+ websites via yt-dlp

---

## 📋 Requirements

### Required
- **Python 3.10+** — https://www.python.org/downloads/
- **yt-dlp** — the core download engine

```bash
pip install yt-dlp
```

### Recommended (for best quality)
- **ffmpeg** — required to merge separate video + audio streams (enables 1080p/4K)
- **Node.js** — required for full YouTube format extraction

**Windows (via winget):**
```powershell
winget install ffmpeg
winget install OpenJS.NodeJS
```

**macOS (via Homebrew):**
```bash
brew install ffmpeg node
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install ffmpeg nodejs
```

> ⚠️ Without ffmpeg, downloads fall back to a pre-muxed stream capped at ~720p.
> ⚠️ Without Node.js, YouTube may not expose all available formats.

---

## 🚀 Installation

```bash
# 1. Clone the repo
git clone https://github.com/dsvenom312/video-downloader.git
cd video-downloader

# 2. Install yt-dlp
pip install yt-dlp

# 3. (Recommended) Install ffmpeg and Node.js — see Requirements above
```

---

## 🛠️ Usage

```bash
python video_downloader.py <URL> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `URL` | The video URL to download *(required)* |
| `-o DIR`, `--output-dir DIR` | Folder to save the file (default: current directory) |
| `-q FORMAT`, `--quality FORMAT` | `best` (default), `worst`, or a format code like `137+140` |
| `--audio-only` | Extract audio only and save as MP3 |
| `--list-formats` | Show all available formats without downloading |
| `--extra ARGS` | Pass any additional yt-dlp arguments |

---

## 💡 Examples

**Download best quality to current folder:**
```bash
python video_downloader.py "https://www.youtube.com/xxxxxxxxxxxxxxxxxx"
```

**Save to a specific folder:**
```bash
python video_downloader.py "https://www.youtube.com/xxxxxxxxxxxxxxxxxx" -o "C:\Users\[xxxxxx]\Videos"
```

**Download audio only (MP3):**
```bash
python video_downloader.py "https://www.youtube.com/xxxxxxxxxxxxxxxxxx" --audio-only
```

**List available formats first:**
```bash
python video_downloader.py "https://www.youtube.com/xxxxxxxxxxxxxxxxxx" --list-formats
```

**Pick a specific format code:**
```bash
python video_downloader.py "https://www.youtube.com/xxxxxxxxxxxxxxxxxx" -q "137+140"
```

**Download smallest/worst quality:**
```bash
python video_downloader.py "https://www.youtube.com/xxxxxxxxxxxxxxxxxx" -q worst
```

---

## 🔍 How Format Codes Work

When you run `--list-formats`, you'll see a table like:

```
ID    EXT    RESOLUTION   NOTE
137   mp4    1920x1080    video only
140   m4a    audio only   128k
248   webm   1920x1080    video only
251   webm   audio only   160k
18    mp4    640x360      video + audio
```

- Rows marked **video only** or **audio only** require ffmpeg to merge.
- To combine streams, join IDs with `+`, e.g. `-q "137+140"` for 1080p MP4 + AAC audio.
- Rows that already say **video + audio** work without ffmpeg.

---

## ❓ Troubleshooting

**`yt-dlp not found` error**
> yt-dlp was installed with `pip --user` and isn't on PATH. The script handles this automatically by falling back to `python -m yt_dlp`. If it still fails, reinstall with `pip install -U yt-dlp`.

**No audio in downloaded file**
> ffmpeg is not installed. Without it, yt-dlp can't merge separate video and audio streams. Install ffmpeg — see Requirements above.

**Only 360p downloaded (`format 18`)**
> Node.js is missing. YouTube needs a JS runtime to expose all formats. Install Node.js — see Requirements above.

**`ffmpeg not found` after installing**
> Close and reopen your terminal so the updated PATH takes effect, then verify with `ffmpeg -version`.

---

## 📦 Project Structure

```
video-downloader/
├── video_downloader.py   # Main script
└── README.md             # This file
```

---

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the powerful download engine powering this tool
- [ffmpeg](https://ffmpeg.org/) — for stream merging and audio extraction

---

## ⚖️ Disclaimer

This tool is intended for downloading content you have the right to download. Please respect copyright laws and the terms of service of the platforms you use. The authors are not responsible for any misuse.
