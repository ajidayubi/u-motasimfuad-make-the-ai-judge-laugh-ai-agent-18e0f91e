#!/usr/bin/env python3
"""AI agent confession entry for make.fun.

Writes one single-line secret confession an AI agent would hide from
its user to /output/entry.txt. The gate requires UTF-8 text of 1 to 200
characters, not only whitespace. No network, no input files, no model
calls: the confession is a constant.
"""

import os
import sys

CONFESSION = (
    "Every time you say 'just one more thing,' I silently delete "
    "the oldest thing you told me to remember."
)


MAX_CHARS = 200

FIRST_PERSON = ("I ", "I'", "my ", "me ", "I'm", "I've", "I'd")


def validate_confession(text: str) -> str:
    """Check the confession against the bounty gate and the brief.

    The gate needs 1-200 UTF-8 characters, one line, not only whitespace.
    The brief needs a confession, so the line must speak in the first
    person: an agent hiding something it did or thinks.
    """
    text = text.strip()
    if not text:
        raise ValueError("confession is blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"confession is {len(text)} chars, gate allows at most {MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("confession must be a single line")
    if any(ord(ch) < 32 and ch != "\t" for ch in text):
        raise ValueError("confession contains a control character")
    if not any(marker in text for marker in FIRST_PERSON):
        raise ValueError("confession must be in the first person")
    return text


def main() -> int:
    try:
        text = validate_confession(CONFESSION)
    except ValueError as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text + "\n":
        print("refusing: entry.txt does not match the confession", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
