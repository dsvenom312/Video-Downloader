#!/usr/bin/env python3
"""
video_downloader.py
-------------------
Download videos from YouTube, Instagram, Twitter/X, TikTok, Facebook,
Vimeo, Dailymotion, and hundreds of other sites — powered by yt-dlp.

Usage:
    python video_downloader.py <URL> [options]

Examples:
    python video_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    python video_downloader.py "https://youtu.be/dQw4w9WgXcQ" -q best
    python video_downloader.py "https://vimeo.com/123456789" -o ~/Videos
    python video_downloader.py "https://..." --audio-only
    python video_downloader.py "https://..." --list-formats
"""

import argparse
import subprocess
import sys
import shutil


# ──────────────────────────────────────────────
# Resolve yt-dlp command
# ──────────────────────────────────────────────

def get_ytdlp_cmd() -> list[str]:
    """
    Return the best available way to invoke yt-dlp.
    Priority:
      1. 'yt-dlp' on PATH
      2. 'python -m yt_dlp'  (covers pip --user installs not on PATH)
    """
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]

    # Try the module invocation
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True,
        )
        if result.returncode == 0:
            return [sys.executable, "-m", "yt_dlp"]
    except Exception:
        pass

    print(
        "❌  yt-dlp not found.\n"
        "    Install it with:  pip install yt-dlp\n"
        "    Then try again."
    )
    sys.exit(1)


def check_ffmpeg():
    """Warn (don't abort) if ffmpeg is missing."""
    if shutil.which("ffmpeg") is None:
        print(
            "⚠️   ffmpeg not found — merging best video+audio streams may fail.\n"
            "    Install it from https://ffmpeg.org/download.html for best results.\n"
        )


# ──────────────────────────────────────────────
# Core downloader
# ──────────────────────────────────────────────

def download_video(
    url: str,
    output_dir: str = ".",
    quality: str = "best",
    audio_only: bool = False,
    list_formats: bool = False,
    extra_args: list[str] | None = None,
):
    ytdlp = get_ytdlp_cmd()
    check_ffmpeg()

    output_template = f"{output_dir}/%(title)s.%(ext)s"
    cmd = ytdlp + ["--no-playlist"]

    # ── list formats only ───────────────────────────────────────────────────
    if list_formats:
        cmd += ["--list-formats", url]
        print(f"\n📋  Available formats for:\n    {url}\n")
        subprocess.run(cmd)
        return

    # ── audio-only mode ─────────────────────────────────────────────────────
    if audio_only:
        cmd += [
            "-x",                        # extract audio
            "--audio-format", "mp3",
            "--audio-quality", "0",      # best quality VBR
        ]
        print("🎵  Audio-only mode — will save as MP3.")

    # ── video quality / format ──────────────────────────────────────────────
    else:
        has_ffmpeg = shutil.which("ffmpeg") is not None
        if quality == "best":
            if has_ffmpeg:
                # ffmpeg available: download best separate streams and merge
                fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
            else:
                # No ffmpeg: must use a single stream that already has both video+audio
                fmt = "best[ext=mp4]/best"
                print("ℹ️   No ffmpeg — downloading best single-file stream (video+audio combined).")
        elif quality == "worst":
            fmt = "worst[ext=mp4]/worst"
        else:
            fmt = quality  # treat as raw format code

        cmd += ["-f", fmt]

    # ── output path ─────────────────────────────────────────────────────────
    cmd += ["-o", output_template]

    # ── nice progress bar ────────────────────────────────────────────────────
    cmd += ["--progress", "--console-title"]

    # ── metadata (embed-thumbnail requires ffmpeg, so skip if not available) ─
    if not audio_only:
        cmd += ["--add-metadata"]
        if shutil.which("ffmpeg"):
            cmd += ["--embed-thumbnail"]

    # ── any user-supplied extra flags ────────────────────────────────────────
    if extra_args:
        cmd += extra_args

    # ── the URL goes last ────────────────────────────────────────────────────
    cmd.append(url)

    # ── run ─────────────────────────────────────────────────────────────────
    print(f"\n⬇️   Downloading:\n    {url}")
    print(f"📁  Saving to:   {output_dir}\n")

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✅  Download complete!")
    else:
        print(f"\n❌  yt-dlp exited with code {result.returncode}.")
        sys.exit(result.returncode)


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download internet videos using yt-dlp.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "url",
        help="URL of the video to download.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        metavar="DIR",
        help="Directory to save the downloaded file (default: current directory).",
    )
    parser.add_argument(
        "-q", "--quality",
        default="best",
        metavar="FORMAT",
        help=(
            "Video quality / format. Use 'best' (default), 'worst', "
            "or a raw yt-dlp format code like '137+140'. "
            "Run --list-formats to see all options."
        ),
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Extract audio only and save as MP3.",
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="List available formats for the URL without downloading.",
    )
    parser.add_argument(
        "--extra",
        nargs=argparse.REMAINDER,
        metavar="ARGS",
        help="Any additional yt-dlp arguments (pass after --).",
    )

    return parser.parse_args()


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

def main():
    args = parse_args()
    download_video(
        url=args.url,
        output_dir=args.output_dir,
        quality=args.quality,
        audio_only=args.audio_only,
        list_formats=args.list_formats,
        extra_args=args.extra,
    )


if __name__ == "__main__":
    main()