# py_subtitle_extractor

[![PyPI version](https://img.shields.io/pypi/v/py_subtitle_extractor.svg)](https://pypi.org/project/py_subtitle_extractor)
[![Python versions](https://img.shields.io/pypi/pyversions/py_subtitle_extractor.svg)](https://pypi.org/project/py_subtitle_extractor)
[![License](https://img.shields.io/pypi/l/py_subtitle_extractor.svg)](https://github.com/re999/py_subtitle_extractor/blob/main/LICENSE)


**Pure-Python MKV subtitle extractor library**  
Zero external dependencies, single-pass streaming, supports raw and SRT output.

---

## 🚀 Features

- **`extract_subtitle_tracks(path)`** → List of subtitle-track metadata (track number, codec, language, name)  
- **`extract_subtitles(path, track)`** → List of `(timestamp_ms, text)` tuples  
- **`extract_subtitles_as_srt(path, track)`** → Complete SRT file as a string  

---

## 📦 Installation

### From PyPI
```bash
pip install py_subtitle_extractor
```

### From source
```bash
git clone https://github.com/re999/py_subtitle_extractor.git
cd py_subtitle_extractor
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip build
pip install .
```

---

## 🛠️ Usage

```python
from py_subtitle_extractor import (
    extract_subtitle_tracks,
    extract_subtitles,
    extract_subtitles_as_srt,
)

# List available subtitle tracks
tracks = extract_subtitle_tracks("movie.mkv")
for t in tracks:
    print(f"Track #{t['track_number']}: {t['codec_id']} [{t['language']}] – {t['name']}")

# Extract raw entries from track #3
entries = extract_subtitles("movie.mkv", 3)
for ts, text in entries:
    print(ts, text)

# Get full SRT text for track #3
srt_text = extract_subtitles_as_srt("movie.mkv", 3)
print(srt_text)
```

---

## 🖥️ CLI Usage

```bash
# List available subtitle tracks via CLI
python -m py_subtitle_extractor movie.mkv

# Extract full SRT from track #3
python -m py_subtitle_extractor movie.mkv -t 3 > subs.srt
```

---

## 📂 Bundling in a Kodi Add-on

Kodi auto-includes `resources/lib` in its Python path. To vendor the library:

```bash
pip install . --upgrade --no-deps -t /path/to/your.addon.id/resources/lib
```

---


## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
