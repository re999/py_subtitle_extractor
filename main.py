import argparse
from py_subtitle_extractor.mkv import extract_subtitle_tracks, extract_subtitles

def parse_args():
    p=argparse.ArgumentParser(description='py_subtitle_extractor')
    p.add_argument('file')
    p.add_argument('-t','--track',type=int,help='track number to dump')
    return p.parse_args()

def main():
    args=parse_args()
    if args.track is None:
        for t in extract_subtitle_tracks(args.file):
            print(f"Track #{t['track_number']}: {t['codec_id']}")
    else:
        subs=extract_subtitles(args.file,args.track)
        for i,(ts,text) in enumerate(subs,1):
            h=ts//3600000; m=(ts%3600000)//60000
            s=(ts%60000)//1000; ms=ts%1000
            start=f"{h:02}:{m:02}:{s:02},{ms:03}"
            print(f"{i}\n{start} --> {start}\n{text}\n")

if __name__=='__main__':
    main()
