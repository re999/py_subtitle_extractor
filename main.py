import argparse
from py_subtitle_extractor.mkv import extract_subtitle_tracks, extract_subtitles

def parse_args():
    p = argparse.ArgumentParser(description="py_subtitle_extractor")
    p.add_argument("file", help="Path to MKV file")
    p.add_argument("-t", "--track", type=int,
                   help="Subtitle track index (1-based) from the list below")
    return p.parse_args()

def main():
    args = parse_args()
    subs = extract_subtitle_tracks(args.file)
    if args.track is None:
        print("Available subtitle tracks:")
        for i, t in enumerate(subs, 1):
            print(f"  {i}: track#{t['track_number']} {t['codec_id']}")
        print("\nThen rerun with `-t INDEX` to dump that subtitle stream.")
    else:
        if args.track < 1 or args.track > len(subs):
            print("Invalid track index.")
            return
        entries = extract_subtitles(args.file, args.track)
        for idx, (ts, text) in enumerate(entries, 1):
            h = ts // 3600000
            m = (ts % 3600000) // 60000
            s = (ts % 60000) // 1000
            ms= ts % 1000
            start = f"{h:02}:{m:02}:{s:02},{ms:03}"
            print(f"{idx}\n{start} --> {start}\n{text}\n")

if __name__ == "__main__":
    main()
