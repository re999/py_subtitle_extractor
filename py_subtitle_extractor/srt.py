from typing import List, Tuple, Iterator

def format_timestamp(ms: int) -> str:
    h, m, s, ms = (
        ms // 3600000,
        (ms % 3600000) // 60000,
        (ms % 60000) // 1000,
        ms % 1000,
    )
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def entries_to_srt(entries: List[Tuple[int, str]]) -> Iterator[str]:
    return (
        f"{i}\n{format_timestamp(ts)} --> {format_timestamp(ts)}\n{text}\n"
        for i, (ts, text) in enumerate(entries, 1)
    )
