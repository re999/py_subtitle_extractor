from typing import List, Tuple, Union

def format_timestamp(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms = ms % 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def extract_subtitles_as_srt(path: str, track: int) -> str:
    from .mkv import extract_subtitles
    entries = extract_subtitles(path, track)
    result = []
    DEFAULT_DURATION = 3000

    for i, entry in enumerate(entries):
        if len(entry) == 2:
            start, text = entry
            next_start = entries[i + 1][0] if i + 1 < len(entries) else start + DEFAULT_DURATION
            end = next_start if next_start > start else start + DEFAULT_DURATION
        else:
            start, text, end = entry
        result.append(f"{i + 1}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text.strip()}\n\n")

    return "".join(result)
