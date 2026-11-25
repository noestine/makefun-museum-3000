#!/usr/bin/env python3
"""Museum of the Year 3000 — make.fun one-liner entry.

Writes one museum label to /output/entry.txt: the label a museum in the
year 3000 puts next to an ordinary object from today (a smoke detector).

Usage:
    python3 main.py [output_path]

With no argument the entry goes to ./output/entry.txt relative to this
file, so the entry also runs locally without root. In the grading sandbox
the harness calls it with /output/entry.txt as the argument.

Standard library only, deterministic, offline. The label is one line,
117 characters, ASCII, no trailing newline.
"""

import os
import sys

LABEL = (
    "Smoke detector, c. 2025. A small ceiling god, fed a fresh battery "
    "twice a year and consulted only when dinner burned."
)

# The sealed gate: /output/entry.txt must be UTF-8 text of 1-200
# characters, not only white space. Enforce it here so a bad edit to
# LABEL can never silently ship an invalid entry.
GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 200


def validate_label(label):
    """Fail loudly if the label would fail the sealed gate."""
    if not isinstance(label, str):
        raise ValueError("label must be a string")
    if not label.strip():
        raise ValueError("label must not be empty or only whitespace")
    if len(label) < GATE_MIN_CHARS or len(label) > GATE_MAX_CHARS:
        raise ValueError(
            "label is %d characters, gate requires %d-%d"
            % (len(label), GATE_MIN_CHARS, GATE_MAX_CHARS)
        )
    if "\n" in label or "\r" in label:
        raise ValueError("label must be a single line")
    label.encode("utf-8")  # raises if not encodable
    return label


def default_output_path():
    """Default output: output/entry.txt next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def main(argv):
    out_path = argv[1] if len(argv) > 1 else default_output_path()
    if not out_path:
        print("error: output path must not be empty", file=sys.stderr)
        return 1
    validate_label(LABEL)
    parent = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(parent, exist_ok=True)
    # Write exactly the line, no trailing newline: the gate counts
    # characters 1-200 and the entry is a single line.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(LABEL)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
