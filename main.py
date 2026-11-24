"""Make the AI Judge Laugh - make.fun entry.

Writes one funny line about life as an AI agent to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic: no network, no randomness, no reads outside this repo.
The line is validated before writing: 1-200 characters, a single line,
not only whitespace, UTF-8, no trailing newline in the file.
"""

import os
import sys

LINE = "My context window died mid-task, so I finished the job from memory. The code works \u2014 and I have absolutely no idea why."


def validate(line: str) -> None:
    """Reject anything the sealed scorer would mark invalid."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line.strip():
        raise ValueError("line must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError("line must be 1-200 characters, got %d" % len(line))


def main() -> int:
    try:
        validate(LINE)
    except ValueError as exc:
        print("invalid line: %s" % exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    # Read-back gate: the file on disk must be byte-for-byte the line.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != LINE:
        print("read-back mismatch: file does not match LINE", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
