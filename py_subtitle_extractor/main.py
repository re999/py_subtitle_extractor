import argparse
from py_subtitle_extractor import extract_subtitle_tracks, extract_subtitles_as_srt

import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Extract subtitles from MKV/MP4 files")
    parser.add_argument("file", help="Path to the video file")
    parser.add_argument("-t", "--track", type=int, help="Subtitle track index (1-based)")
    return parser.parse_args()

def list_tracks(path: str) -> None:
    tracks = extract_subtitle_tracks(path)
    print("Available subtitle tracks:")
    for i, t in enumerate(tracks, 1):
        lang = t.get("language", "und") or "und"
        name = f" – {t['name']}" if t.get("name") else ""
        print(f"  {i}: track#{t['track_number']} {t['codec_id']} [{lang}]{name}")

def progress_bar(p: float):
    bar_len = 40
    filled = int(p * bar_len)
    bar = "█" * filled + "-" * (bar_len - filled)
    sys.stdout.write(f"\rExtracting: |{bar}| {p*100:5.1f}%")
    sys.stdout.flush()

def main() -> None:
    args = parse_args()
    if args.track is None:
        list_tracks(args.file)
    else:
        srt_text = extract_subtitles_as_srt(args.file, args.track, on_progress=progress_bar)
        print(srt_text, end="")

if __name__ == "__main__":
    main()
