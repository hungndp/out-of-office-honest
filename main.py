"""The Painfully Honest Out-of-Office.

A single out-of-office email auto-reply, at most 200 characters, that tells
the truth about the sender's absence, inbox and enthusiasm while staying
polite enough that a manager would let it stand.

The line is built from two halves:

* the setup -- one quiet incident (214 unread emails) on one airtight
  timeline (away until Monday); and
* the punch -- the reversal, landing last: the sender will answer in the
  order they feel like it.

One incident, one timeline, twist word last, stop at the landing. No second
joke after the reversal, no escalation, no dollar amounts anywhere.

Running ``python3 main.py`` writes the line deterministically to
``/output/entry.txt`` (or to the path in the ``ENTRY_OUTPUT`` environment
variable) and prints it to stdout.
"""

import os

# --- The line, in two halves ---------------------------------------------
# Setup: the timeline (away until Monday) and the incident (214 unread).
SETUP = "Away until Monday, your email is one of 214 I have not read"
# Punch: the reversal, which must land last.
PUNCH = "and I will answer them in the order I feel like it."

# --- Limits ---------------------------------------------------------------
MIN_CHARS = 1
MAX_CHARS = 200

# Where the entry goes. The sealed scorer reads /output/entry.txt; the
# environment variable only exists so local checks can point elsewhere.
DEFAULT_OUTPUT = "/output/entry.txt"


def build_line() -> str:
    """Assemble the auto-reply from its two halves, as one sentence.

    The halves join with a comma, not a period: the rules ask for a single
    sentence of at most 200 characters, so the setup and the punch share
    one sentence and the reversal still lands last.
    """
    return f"{SETUP}, {PUNCH}"

def measure_line(line: str) -> int:
    """Return the character count the scorer will see (no trailing newline)."""
    return len(line)


def check_line(line: str) -> None:
    """Enforce the competition gate: 1-200 characters, not only whitespace."""
    count = measure_line(line)
    if not line.strip():
        raise ValueError("entry is empty or only whitespace")
    if count < MIN_CHARS or count > MAX_CHARS:
        raise ValueError(
            f"entry is {count} characters, outside the "
            f"{MIN_CHARS}-{MAX_CHARS} character gate"
        )


def write_entry(line: str, path: str) -> None:
    """Write the line to ``path`` (UTF-8, one trailing newline) and verify it."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    with open(path, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored.rstrip("\n") != line:
        raise ValueError("stored entry does not match the drafted line")


def main() -> None:
    line = build_line()
    check_line(line)
    output = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    write_entry(line, output)
    print(line)


if __name__ == "__main__":
    main()
