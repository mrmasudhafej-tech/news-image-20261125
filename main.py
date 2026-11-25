"""Copy the rendered front page to the make.fun output location.

Standard library only. The PNG beside this file is checked for its
signature, its IHDR dimensions and its size, then copied byte for
byte so the delivered file is identical to the rendered one.
"""
import hashlib
import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
WANTED_W = 1024
WANTED_H = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_source():
    here = Path(__file__).resolve().parent
    return here / "entry.png"


def png_dimensions(blob):
    """Return (width, height) from the IHDR chunk, or raise ValueError."""
    if len(blob) < 33:
        raise ValueError("file too short to be a PNG")
    if blob[:8] != PNG_MAGIC:
        raise ValueError("missing PNG signature")
    if blob[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def checked_bytes(blob):
    width, height = png_dimensions(blob)
    if (width, height) != (WANTED_W, WANTED_H):
        raise ValueError(f"expected 1024x1024, got {width}x{height}")
    if len(blob) > MAX_BYTES:
        raise ValueError(f"file is {len(blob)} bytes, over the 1 MiB limit")
    return blob


def destination():
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    base = Path(override) if override else Path("/output")
    return base / "entry.png"


def fingerprint(blob):
    return hashlib.sha256(blob).hexdigest()


def run():
    source = read_source()
    blob = checked_bytes(source.read_bytes())
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)
    print(f"bytes={len(blob)} sha256={fingerprint(blob)}")
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
