from py_subtitle_extractor.mkv import extract_subtitles_from_mkv

if __name__ == "__main__":
    path = "example.mkv"
    subs = extract_subtitles_from_mkv(path)
    for sub in subs:
        print(sub.to_srt())
