# Video Frame Extractor

Extract evenly spaced frames from MP4 videos using Python. Supports recursive search, custom number of frames, frames-per-minute, and dry-run mode.

## Features

- Extract a fixed number of evenly spaced frames per video
- Extract frames per minute of video (`--per-minute`)
- Recursive search for MP4 files (`-R`)
- Output frames into `<videoName>_out` folders next to each video
- Filenames contain timestamp in `HH_MM_SS` format
- Dry-run mode to preview what would be extracted (`--dry-run`)
- Cross-platform: Windows/macOS/Linux

## Requirements

- Python 3.7+
- `ffmpeg` and `ffprobe` installed and on your PATH

## Usage

```bash
# Extract default 20 frames per video
python extract_frames.py "path/to/videos"

# Extract 50 frames per video
python extract_frames.py "path/to/videos" -n 50

# Extract 5 frames per minute of video, recursively
python extract_frames.py "path/to/videos" --per-minute 5 -R

# Dry-run to preview
python extract_frames.py "path/to/videos" -R --dry-run
