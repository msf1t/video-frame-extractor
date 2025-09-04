#!/usr/bin/env python3
import subprocess
from pathlib import Path
import math
import sys
import argparse

def get_duration(video_path: Path) -> float:
    """Get video duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {video_path}: {result.stderr}")
    return float(result.stdout.strip())

def extract_frames(video_path: Path, num_frames: int, dry_run: bool = False):
    """Extract evenly spaced frames from a video."""
    outdir = video_path.parent / f"{video_path.stem}_out"
    outdir.mkdir(exist_ok=True)
    
    duration = get_duration(video_path)
    
    for i in range(1, num_frames + 1):
        ts = math.floor(i * duration / (num_frames + 1))
        ts_h = ts // 3600
        ts_m = (ts % 3600) // 60
        ts_s = ts % 60
        ts_str = f"{ts_h:02}_{ts_m:02}_{ts_s:02}"
        outfile = outdir / f"{ts_str}.jpg"
        
        print(f"[{'DRY-RUN' if dry_run else 'EXTRACT'}] {video_path.name} -> {outfile} at {ts} sec")
        if not dry_run:
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(ts), "-i", str(video_path),
                "-frames:v", "1", "-q:v", "2", str(outfile)
            ], check=True)

def collect_videos(input_path: Path, recursive: bool):
    """Collect all MP4 files under input_path, case-insensitive."""
    if recursive:
        mp4_files = [f for f in input_path.rglob("*") if f.suffix.lower() == ".mp4"]
    else:
        mp4_files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() == ".mp4"]
    return mp4_files

def main():
    parser = argparse.ArgumentParser(
        description="Extract evenly spaced frames from MP4 videos."
    )
    parser.add_argument("input_path", type=Path, help="Directory containing MP4 videos")
    parser.add_argument("-R", "--recursive", action="store_true",
                        help="Recursively search for MP4 files in subdirectories")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--frames", type=int, default=20,
                       help="Number of frames per video (default: 20)")
    group.add_argument("--per-minute", type=int,
                       help="Number of frames per minute of video (mutually exclusive with -n)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be extracted without running ffmpeg")
    
    args = parser.parse_args()
    
    if not args.input_path.exists():
        print(f"⚠️ Input path does not exist: {args.input_path}")
        sys.exit(1)

    videos = collect_videos(args.input_path, args.recursive)
    if not videos:
        print(f"⚠️ No MP4 files found in {args.input_path}")
        sys.exit(1)

    for video in videos:
        try:
            duration = get_duration(video)
            if args.per_minute:
                num_frames = max(1, round(args.per_minute * (duration / 60)))
            else:
                num_frames = args.frames
            extract_frames(video, num_frames, dry_run=args.dry_run)
        except Exception as e:
            print(f"⚠️ Error processing {video}: {e}")

if __name__ == "__main__":
    main()
