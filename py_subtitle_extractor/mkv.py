from .ebml import read_id, read_size, read_vint
from typing import List, Tuple, BinaryIO

SEGMENT      = 0x18538067
TRACKS       = 0x1654AE6B
CLUSTER      = 0x1F43B675
TIMECODE     = 0xE7
SIMPLEBLOCK  = 0xA3
BLOCKGROUP   = 0xA0
BLOCK        = 0xA1

def _read_header(f: BinaryIO) -> Tuple[int, int]:
    eid, _ = read_id(f)
    sz, _  = read_size(f)
    return eid, sz

def extract_subtitle_tracks(path: str) -> List[dict]:
    with open(path, "rb") as f:
        _, h = _read_header(f); f.seek(h, 1)
        eid, h = _read_header(f)
        if eid != SEGMENT:
            return []
        end = f.tell() + h
        while f.tell() < end:
            eid, sz = _read_header(f)
            if eid == TRACKS:
                return [t for t in _parse_tracks(f.read(sz)) if t["type"] == 0x11]
            f.seek(sz, 1)
    return []

def _parse_tracks(data: bytes) -> List[dict]:
    from io import BytesIO
    buf = BytesIO(data); out = []
    while True:
        try:
            eid, sz = _read_header(buf)
        except EOFError:
            break
        chunk = buf.read(sz)
        if eid == 0xAE:  # TRACKENTRY
            out.append(_parse_track_entry(chunk))
    return out

def _parse_track_entry(data: bytes) -> dict:
    from io import BytesIO
    buf = BytesIO(data)
    info = {"type": 0, "track_number": 0, "codec_id": ""}
    while True:
        try:
            eid, sz = _read_header(buf)
        except EOFError:
            break
        v = buf.read(sz)
        if eid == 0x83:    info["type"]         = v[0]
        if eid == 0xD7:    info["track_number"] = int.from_bytes(v, "big")
        if eid == 0x86:    info["codec_id"]     = v.decode("ascii", "ignore")
    return info

def extract_subtitles(path: str, track: int) -> List[Tuple[int, str]]:
    subs: List[Tuple[int, str]] = []
    with open(path, "rb") as f:
        _, h = _read_header(f); f.seek(h, 1)
        eid, h = _read_header(f)
        if eid != SEGMENT:
            return subs
        seg_end = f.tell() + h
        while f.tell() < seg_end:
            eid, sz = _read_header(f)
            if eid == CLUSTER:
                subs += _parse_cluster(f, sz, track)
            else:
                f.seek(sz, 1)
    return subs

def _parse_cluster(f: BinaryIO, size: int, track: int) -> List[Tuple[int, str]]:
    end = f.tell() + size
    base = _read_cluster_time(f, end)
    out: List[Tuple[int, str]] = []
    while f.tell() < end:
        eid, sz = _read_header(f)
        if eid == SIMPLEBLOCK:
            out += _handle_block(f, sz, base, track)
        elif eid == BLOCKGROUP:
            out += _handle_group(f, sz, base, track)
        else:
            f.seek(sz, 1)
    return out

def _read_cluster_time(f: BinaryIO, end: int) -> int:
    while f.tell() < end:
        eid, sz = _read_header(f)
        if eid == TIMECODE:
            return int.from_bytes(f.read(sz), "big")
        f.seek(sz, 1)
    return 0

def _handle_block(f: BinaryIO, size: int, base: int, track: int) -> List[Tuple[int, str]]:
    trk, vlen = read_vint(f)
    t = int.from_bytes(f.read(2), "big", signed=True)
    f.read(1)
    payload = f.read(size - vlen - 3)
    return [(base + t, payload.decode("utf-8", "ignore").strip())] if trk == track else []

def _handle_group(f: BinaryIO, size: int, base: int, track: int) -> List[Tuple[int, str]]:
    end = f.tell() + size
    out: List[Tuple[int, str]] = []
    while f.tell() < end:
        eid, sz = _read_header(f)
        if eid == BLOCK:
            out += _handle_block(f, sz, base, track)
        else:
            f.seek(sz, 1)
    return out
