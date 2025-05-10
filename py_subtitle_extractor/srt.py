from typing import List, Tuple, Iterator
from py_subtitle_extractor.mkv import extract_subtitles

def format_timestamp(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms_rem = ms % 1000
    return f"{h:02}:{m:02}:{s:02},{ms_rem:03}"

def entries_to_srt(entries: List[Tuple[int, str]]) -> Iterator[str]:
    for i in range(len(entries) - 1):
        start = entries[i][0]
        end = entries[i + 1][0]
        if start == end:
            end += 2000
        yield f"{i + 1}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{entries[i][1]}\n\n"


from collections import defaultdict

def extract_subtitles_as_srt(path: str, track: int) -> str:
    entries = extract_subtitles(path, track)
    result = []
    DEFAULT_DURATION = 3000

    for i, (ts, text) in enumerate(entries):
        start = ts
        end = entries[i + 1][0] if i + 1 < len(entries) else start + DEFAULT_DURATION
        if end <= start:
            end = start + DEFAULT_DURATION
        result.append(f"{i + 1}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n\n")

    return ''.join(result)

