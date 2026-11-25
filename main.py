#!/usr/bin/env python3
"""Copy the finished front page for 25 November 2026 to the output dir.

The image itself lives in this repository as ``entry.png``. It was drawn
for this competition day by ``render.py`` (Pillow, run locally while
building the entry). This program does no drawing and needs no network:
it checks the stored PNG, then writes the same bytes to
``/output/entry.png`` (or to ``$MAKEFUN_OUTPUT_DIR`` when set), so the
grader's two runs always produce identical output. Standard library only.
The PNG is validated before it is copied, so a damaged or wrong-sized
stored image fails loudly instead of producing a bad entry.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def choose_output_dir() -> Path:
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(override) if override else Path("/output")


def load_image(repo_dir: Path) -> bytes:
    source = repo_dir / IMAGE_NAME
    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"{IMAGE_NAME} is {len(data)} bytes, over the 1 MiB limit"
        )
    if not data.startswith(PNG_MAGIC):
        raise SystemExit(f"{IMAGE_NAME} does not start with a PNG signature")
    if b"IEND" not in data[-12:]:
        raise SystemExit(f"{IMAGE_NAME} does not end with an IEND chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"expected 1024x1024, found {width}x{height}")
    return data


def main() -> int:
    repo_dir = Path(__file__).resolve().parent
    data = load_image(repo_dir)
    out_dir = choose_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE_NAME
    target.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
