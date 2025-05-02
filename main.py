import argparse
from py_subtitle_extractor.mkv import extract_subtitle_tracks, extract_subtitles
from py_subtitle_extractor.srt import entries_to_srt

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("-t", "--track", type=int)
    return p.parse_args()

def list_tracks(path):
    for i, t in enumerate(extract_subtitle_tracks(path), 1):
        lang = t["language"] or "und"
        name = f" – {t['name']}" if t["name"] else ""
        print(f"  {i}: track#{t['track_number']} {t['codec_id']} [{lang}]{name}")

def main():
    args = parse_args()
    if not args.track:
        print("Available subtitle tracks:")
        list_tracks(args.file)
        return
    entries = extract_subtitles(args.file, args.track)
    for line in entries_to_srt(entries):
        print(line, end="")

if __name__ == "__main__":
    main()
