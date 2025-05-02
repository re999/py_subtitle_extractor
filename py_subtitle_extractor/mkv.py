from .ebml import read_id, read_size, read_vint
from typing import List, Tuple

SEGMENT_ID      = 0x18538067
TRACKS_ID       = 0x1654AE6B
TRACKENTRY_ID   = 0xAE
TRACKTYPE_ID    = 0x83
TRACKNUMBER_ID  = 0xD7
CODECID_ID      = 0x86
CLUSTER_ID      = 0x1F43B675
TIMECODE_ID     = 0xE7
SIMPLEBLOCK_ID  = 0xA3
BLOCKGROUP_ID   = 0xA0
BLOCK_ID        = 0xA1

def _read_header(f):
    eid, _ = read_id(f)
    sz,  _ = read_size(f)
    return eid, sz

def extract_subtitle_tracks(path: str) -> List[dict]:
    from io import BytesIO
    out = []
    with open(path, "rb") as f:
        _, sz = _read_header(f); f.seek(sz, 1)
        eid, sz = _read_header(f)
        if eid != SEGMENT_ID:
            return []
        seg_end = f.tell() + sz
        while f.tell() < seg_end:
            eid, sz = _read_header(f)
            if eid == TRACKS_ID:
                data = f.read(sz)
                out = _parse_tracks(data)
                break
            f.seek(sz, 1)
    return [t for t in out if t["type"] == 0x11]

def extract_subtitles(path: str, track: int) -> List[Tuple[int, str]]:
    subs: List[Tuple[int, str]] = []
    with open(path, "rb") as f:
        # skip EBML header + go into Segment
        _, sz = _read_header(f); f.seek(sz, 1)
        eid, sz = _read_header(f)
        if eid != SEGMENT_ID:
            return subs
        seg_end = f.tell() + sz

        # streaming po klastrach
        while f.tell() < seg_end:
            eid, sz = _read_header(f)
            if eid != CLUSTER_ID:
                f.seek(sz, 1)
                continue
            cluster_end = f.tell() + sz
            cluster_time = 0

            # parsujemy elementy klastra w jednym przebiegu
            while f.tell() < cluster_end:
                eid2, sz2 = _read_header(f)
                if eid2 == TIMECODE_ID:
                    cluster_time = int.from_bytes(f.read(sz2), "big")
                elif eid2 == SIMPLEBLOCK_ID:
                    trk, vlen = read_vint(f)
                    t = int.from_bytes(f.read(2), "big", signed=True)
                    f.read(1)
                    payload_len = sz2 - vlen - 3
                    if trk == track:
                        txt = f.read(payload_len).decode("utf-8", "ignore").strip()
                        subs.append((cluster_time + t, txt))
                    else:
                        f.seek(payload_len, 1)
                elif eid2 == BLOCKGROUP_ID:
                    group_end = f.tell() + sz2
                    while f.tell() < group_end:
                        eid3, sz3 = _read_header(f)
                        if eid3 == BLOCK_ID:
                            trk, vlen = read_vint(f)
                            t = int.from_bytes(f.read(2), "big", signed=True)
                            f.read(1)
                            payload_len = sz3 - vlen - 3
                            if trk == track:
                                txt = f.read(payload_len).decode("utf-8", "ignore").strip()
                                subs.append((cluster_time + t, txt))
                            else:
                                f.seek(payload_len, 1)
                        else:
                            f.seek(sz3, 1)
                else:
                    f.seek(sz2, 1)
    return subs

def _parse_tracks(data: bytes) -> List[dict]:
    from io import BytesIO
    buf = BytesIO(data)
    out = []
    while True:
        try:
            eid, sz = _read_header(buf)
        except EOFError:
            break
        chunk = buf.read(sz)
        if eid == TRACKENTRY_ID:
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
        if eid == TRACKTYPE_ID:
            info["type"] = v[0]
        if eid == TRACKNUMBER_ID:
            info["track_number"] = int.from_bytes(v, "big")
        if eid == CODECID_ID:
            info["codec_id"] = v.decode("ascii", "ignore")
    return info
