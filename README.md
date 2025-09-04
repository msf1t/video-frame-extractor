# Video Frame Extractor

Extract frames from MP4 videos into a **single output directory**, with options for recursion, frames-per-minute, and dry-run mode.

## Features

- Extract a fixed number of evenly spaced frames per video (`-n`)
- Extract frames per minute of video (`--per-minute`)
- Recursive search for MP4 files (`-R`)
- Output all frames into a **single directory** with filenames: `videoName_HH_MM_SS.jpg`
- Dry-run mode to preview what would be extracted (`--dry-run`)
- Cross-platform: Windows/macOS/Linux

## Requirements

- Python 3.7+
- `ffmpeg` and `ffprobe` installed and on your PATH

## Usage

```bash
# Default: 20 frames per video, output to same folder as video
python extract_frames.py "path/to/videos"

# Recursive search
python extract_frames.py "path/to/videos" -R

# Extract 50 frames per video into a single folder
python extract_frames.py "path/to/videos" -n 50 -o "path/to/frames"

# Extract 5 frames per minute, recursively, into a single folder
python extract_frames.py "path/to/videos" --per-minute 5 -R -o "path/to/frames"

# Dry-run to preview without writing files
python extract_frames.py "path/to/videos" -R --dry-run
