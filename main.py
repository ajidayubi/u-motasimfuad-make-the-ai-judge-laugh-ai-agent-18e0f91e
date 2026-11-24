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


def main() -> int:
    text = CONFESSION.strip()
    if not text:
        print("refusing: confession is blank", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"refusing: confession is {len(text)} chars, gate allows at most 200",
              file=sys.stderr)
        return 1
    if "\n" in text:
        print("refusing: confession must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 and ch != "\t" for ch in text):
        print("refusing: confession contains a control character", file=sys.stderr)
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
