from typing import List, Tuple, Iterator
from py_subtitle_extractor.mkv import extract_subtitles

def format_timestamp(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms_rem = ms % 1000
    return f"{h:02}:{m:02}:{s:02},{ms_rem:03}"

def entries_to_srt(entries: List[Tuple[int, str]]) -> Iterator[str]:
    for idx, (ts, text) in enumerate(entries, 1):
        stamp = format_timestamp(ts)
        yield f"{idx}\n{stamp} --> {stamp}\n{text}\n"

def extract_subtitles_as_srt(path: str, track: int) -> str:
    return "".join(entries_to_srt(extract_subtitles(path, track)))
