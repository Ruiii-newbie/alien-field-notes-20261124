"""Alien Field Notes: The Two Day Earth Review — make.fun bounty entry.

Writes one original line, an alien tourist's review of planet Earth,
to /output/entry.txt. Stdlib only.

The program validates the line before writing and verifies the file
afterwards by reading it back, so a bad write can never pass silently.
"""

import hashlib
import os

ENTRY_LINE = (
    "Three stars: beautiful blue planet, but the locals invented Monday, "
    "queue for coffee like a sacred ritual, and nobody could explain "
    "the weather."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(line: str) -> None:
    """The entry must be exactly one line, at most 200 chars, not blank."""
    if not line.strip():
        raise ValueError("entry line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")


def write_entry() -> bytes:
    """Write the entry with a deterministic LF line ending; return bytes."""
    validate(ENTRY_LINE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    payload = (ENTRY_LINE + "\n").encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(payload)
    return payload


def verify_written(expected: bytes) -> None:
    """Read the file back and confirm it is byte-identical and valid."""
    with open(OUTPUT_PATH, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise ValueError("verification failed: /output/entry.txt differs")
    text = actual.decode("utf-8")
    validate(text.rstrip("\n"))
    if text.count("\n") != 1:
        raise ValueError("verification failed: file must hold exactly one line")


def main() -> None:
    payload = write_entry()
    verify_written(payload)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {len(ENTRY_LINE)} chars to {OUTPUT_PATH}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
