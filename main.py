"""One Word, First Thought.

Writes a single word -- the first word that comes to mind -- to
``entry.txt`` inside the output directory. Nothing else.

The word is chosen once, up front, and never recomputed: the whole
point of the entry is that it is a single unedited first thought.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

# The first word that came to mind. One word, letters only, no edits.
WORD = "firefly"


def validate(word: str) -> str:
    """Enforce the entry rules; raise ValueError on any violation."""
    if not word:
        raise ValueError("word must not be empty")
    if len(word.split()) != 1:
        raise ValueError("word must be exactly one word")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must be exactly one word (no whitespace)")
    if not word.isalpha():
        raise ValueError("word must contain letters only")
    if not word.isascii():
        raise ValueError("word must contain ASCII letters only")
    return word


def output_path() -> Path:
    """Resolve the output directory from the environment, default /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.txt"


def main() -> int:
    word = validate(WORD)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = word.encode("utf-8")
    path.write_bytes(data)
    # Round-trip check: what we wrote must read back as exactly the word.
    if path.read_bytes() != data:
        raise RuntimeError(f"round-trip mismatch writing {path}")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}: {word} (sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
