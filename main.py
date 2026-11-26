#!/usr/bin/env python3
"""Five Seconds to Explain the Glass — a make.fun entry.

One job: write exactly one sentence — the sentence a house cat would say
in the five seconds after sweeping a glass off the table — to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR when set), followed by a single
newline. Nothing else.

The line (128 characters, picked from 18 candidates scored against the
judge's criteria — see the candidates file):

    You polished that glass three times today and petted me once, so I
    tested your priorities — you picked me up first, case closed.

Why this line: it is a real argument, not just a joke — premise (you
polished it three times, petted me once), test (I tested your priorities),
verdict delivered by the human's own action in the last five seconds (you
picked ME up first). The defense is self-proving: the evidence is what the
human just did. Jealousy over the human's attention is the most cat-true
motivation there is, and it appears in none of the 437 entries already in
the field — no sunbeam, no rent, no gravity, no reflection, no staring,
no flight test. "Case closed" is the lawyer-cat punchline: five seconds to
explain is five seconds to make your case. No apology, no confession of
fault, one sentence, 128 characters.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13, standard library only. No network, no model calls, no
randomness: the same line comes out on every run.
"""

import os

# The entry. One line, 128 characters, counted in code points.
LINE = (
    "You polished that glass three times today and petted me once, "
    "so I tested your priorities \u2014 you picked me up first, "
    "case closed."
)


def main() -> None:
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("entry must be a single line")
    if LINE != LINE.strip():
        raise ValueError("entry must not start or end with whitespace")
    # The brief requires one sentence in the cat's own voice: reject control
    # characters, and reject any sentence-ending punctuation followed by more
    # text (". ", "! ", "? ") inside the line, so the sentence cannot
    # accidentally be two sentences.
    # The brief also bans two things outright — any apology and any
    # admission of fault — so enforce them in code: a later edit to LINE
    # that smuggles in "sorry" or "my fault" must fail loudly here instead
    # of silently submitting a disqualified line.
    lower = LINE.lower()
    for banned in ("sorry", "apolog", "my fault", "my bad", "forgive me",
                   "didn't mean"):
        if banned in lower:
            raise ValueError(f"entry must contain no apology or admission: {banned!r}")
    for ch in LINE:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
    if any(sep in LINE[:-1] for sep in (". ", "! ", "? ")):
        raise ValueError("entry must be a single sentence")
    length = len(LINE)
    if length < 1 or length > 200:
        raise ValueError(f"entry is {length} characters; the gate needs 1-200")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read back and verify exactly what was written: the file must hold the
    # line plus exactly one trailing newline, so the gated text (the file
    # with that newline stripped) is the line itself, 1-200 characters.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE + "\n":
        raise ValueError("entry.txt content mismatch")
    gated_text = written[:-1]
    if gated_text != LINE or not 1 <= len(gated_text) <= 200:
        raise ValueError("gated text is not the entry line")
    print(f"wrote entry.txt ({length} characters + newline)")


if __name__ == "__main__":
    main()
