# Universal Video Downloader

**Universal Video Downloader** is a desktop tool designed to download videos directly from the internet using a clean and ad-free interface. It was built to provide a simple, professional alternative to web-based downloaders that often include invasive ads, misleading buttons, and questionable redirects.

## Features

- Clean and professional user interface (dark mode)
- Splash screen with custom branding
- Download YouTube videos in high quality (up to 1080p+)
- Merges video and audio streams automatically
- No ads, no pop-ups, no tracking
- Supports multiple formats via yt-dlp
- FFmpeg is automatically downloaded and configured
- Animated neon progress bar
- Compatible with Windows (tested on Python 3.10+)

## Why this project

Most video downloader websites are filled with aggressive advertising, popups, fake download buttons, and sometimes malware. This project was created to offer a straightforward, user-friendly application that respects the user’s attention and device.

## Requirements

- Python 3.10 or later
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/) (automatically downloaded)
- tkinter (built-in on most Python distributions)
- Pillow (for image rendering)

## Installation

You can run it directly from source:

```bash
pip install yt-dlp pillow
python vdown.py