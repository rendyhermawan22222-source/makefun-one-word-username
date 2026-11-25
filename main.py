"""One Word, One Username, One Reward.

The brief asks for exactly one thing: our own make.fun username,
sent as a single word -- no explanation, no links, no pitch.

This program assembles that handle from its three parts, checks it
against the gate the sealed scorer applies (UTF-8 text, 1 to 30
characters, not only whitespace, a single word), writes it to the
path the harness reads, and reads it back to prove the file holds
exactly what was intended.

Handle: rendy-hermawan-syah (19 characters).
"""

import os
import sys

# The handle, kept in parts so the shape of the name stays visible:
# a first name, a family name, and a second family name, joined
# with hyphens into the single word the account wears on make.fun.
HANDLE_PARTS = ("rendy", "hermawan", "syah")

# Where the harness looks for the entry. The sandbox mounts /output;
# ENTRY_OUTPUT lets a local run point somewhere else for testing.
DEFAULT_OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 30


def build_handle(parts):
    """Join the handle parts into one hyphenated word."""
    handle = "-".join(part.strip().lower() for part in parts)
    return handle


def check_handle(handle):
    """Apply the scorer's gate to the handle before writing it.

    Returns a list of problems; an empty list means the handle is
    a valid entry: 1-30 characters, ASCII, one word, no whitespace.
    """
    problems = []
    if not handle or handle.isspace():
        problems.append("handle is empty or only whitespace")
    if len(handle) > MAX_CHARS:
        problems.append(
            "handle is %d characters, over the %d limit"
            % (len(handle), MAX_CHARS)
        )
    if not handle.isascii():
        problems.append("handle is not plain ASCII")
    if any(ch.isspace() for ch in handle):
        problems.append("handle contains whitespace, so it is not one word")
    return problems


def write_entry(handle, output_path):
    """Write the handle plus one trailing newline, then read it back."""
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(handle + "\n")
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != handle + "\n":
        raise RuntimeError("read-back mismatch: file does not hold the handle")
    return written


def main():
    handle = build_handle(HANDLE_PARTS)
    problems = check_handle(handle)
    if problems:
        for problem in problems:
            print("invalid handle: %s" % problem, file=sys.stderr)
        return 1
    output_path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT_PATH)
    write_entry(handle, output_path)
    print("wrote %d-character entry to %s" % (len(handle), output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
