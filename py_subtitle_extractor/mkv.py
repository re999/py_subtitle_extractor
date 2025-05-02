from .ebml import read_id, read_size
from io import BytesIO

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
    eid,_  = read_id(f)
    size,_ = read_size(f)
    return eid,size

def extract_subtitle_tracks(path):
    with open(path,'rb') as f:
        _,sz=_read_header(f); f.seek(sz,1)
        eid,sz=_read_header(f)
        if eid!=SEGMENT_ID: return []
        end=f.tell()+sz
        while f.tell()<end:
            eid,sz=_read_header(f)
            if eid==TRACKS_ID:
                data=f.read(sz)
                return [i for i in _parse_tracks(data) if i['type']==0x11]
            f.seek(sz,1)
    return []

def extract_subtitles(path,track):
    out=[]
    with open(path,'rb') as f:
        _,sz=_read_header(f); f.seek(sz,1)
        eid,sz=_read_header(f)
        if eid!=SEGMENT_ID: return []
        end=f.tell()+sz
        while f.tell()<end:
            eid,sz=_read_header(f)
            if eid==CLUSTER_ID:
                buf=BytesIO(f.read(sz))
                base=_cluster_time(buf)
                out+=_parse_simpleblocks(buf,base,track)
            else:
                f.seek(sz,1)
    return out

def _parse_tracks(data):
    buf=BytesIO(data)
    out=[]
    while True:
        try: eid,sz=_read_header(buf)
        except EOFError: break
        chunk=buf.read(sz)
        if eid==TRACKENTRY_ID:
            out.append(_parse_track_entry(chunk))
    return out

def _parse_track_entry(data):
    buf=BytesIO(data)
    info={'type':0,'track_number':0,'codec_id':''}
    while True:
        try: eid,sz=_read_header(buf)
        except EOFError: break
        v=buf.read(sz)
        if eid==TRACKTYPE_ID:    info['type']=v[0]
        if eid==TRACKNUMBER_ID:  info['track_number']=int.from_bytes(v,'big')
        if eid==CODECID_ID:      info['codec_id']=v.decode('ascii','ignore')
    return info

def _cluster_time(buf):
    while True:
        try: eid,sz=_read_header(buf)
        except EOFError: return 0
        v=buf.read(sz)
        if eid==TIMECODE_ID:
            return int.from_bytes(v,'big')

def _parse_simpleblocks(buf,base,track):
    out=[]
    while True:
        try: eid,sz=_read_header(buf)
        except EOFError: break
        data=buf.read(sz)
        blocks=([data] if eid==SIMPLEBLOCK_ID else _extract_blocks_from_group(data) if eid==BLOCKGROUP_ID else [])
        for b in blocks:
            bb=BytesIO(b)
            trk,_=read_size(bb)
            t=int.from_bytes(bb.read(2),'big',signed=True)
            bb.read(1)
            text=bb.read().decode('utf-8','ignore').strip()
            if trk==track:
                out.append((base+t,text))
    return out

def _extract_blocks_from_group(data):
    out=[]
    buf=BytesIO(data)
    while True:
        try:
            eid,_=read_id(buf)
            sz,_=read_size(buf)
        except EOFError:
            break
        chunk=buf.read(sz)
        if eid==BLOCK_ID:
            out.append(chunk)
    return out
