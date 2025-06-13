# Universal Video Downloader

**Universal Video Downloader** is a desktop tool designed to download videos directly from the internet using a clean and ad-free interface. It was built to provide a simple alternative to web-based downloaders that often include invasive ads, misleading buttons, and questionable redirects.

## Features

- Clean user interface (dark mode)
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

---

## How to Use

### Option 1: Run the executable (recommended for most users)

If you do not want to install Python or any dependencies, simply navigate to the `dist` folder and run the executable file:

```bash
vdown.exe
```

> This file is standalone and includes all dependencies and the application icon. No internet is required after first launch (FFmpeg is downloaded automatically only once if not present).

---

### Option 2: Run the Python script manually

If you prefer to run the source code directly:

#### Step 1: Install Python 3.10 or later

You can download it from: https://www.python.org/downloads/

Make sure to check the box **“Add Python to PATH”** during installation.

#### Step 2: Install the required libraries

Open a terminal and run:

```bash
pip install yt-dlp pillow
```

These libraries are required:
- `yt-dlp` – for downloading videos
- `pillow` – for image/splash rendering

#### Step 3: Run the application

Once dependencies are installed, run:

```bash
python vdown.py
```

---

## Building the executable (for developers)

To generate a `.exe` with your own icon and splash:

```bash
pyinstaller --noconsole --onefile --icon=icon.ico vdown.py
```

The final file will be available in the `dist` folder.

---
