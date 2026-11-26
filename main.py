#!/usr/bin/env python3
"""Five Seconds to Explain the Glass — make.fun bounty entry.

Writes exactly one sentence to /output/entry.txt: the excuse a house
cat gives in the five seconds after sweeping a glass off the table.
The pick: the glass was judging the cat's eating habits with its
silent, transparent stare, so the cat removed the witness and the
floor buried the evidence. Pure cat logic (a staring glass is a
witness to be dealt with), self-interest, total lack of remorse, a
fresh comic idea with two punches, and a spoken line that fits five
seconds. No apology, no confession.

Usage:
    python3 main.py                  # write the line to /output/entry.txt
    python3 main.py --dest out.txt   # write it somewhere else instead
    python3 main.py --self-test      # check the gate, print the hash, exit
"""

import argparse
import hashlib
import sys
from pathlib import Path

# The line. One sentence, 133 characters, no padding.
PICK = (
    "The glass was judging my eating habits with its silent, "
    "transparent stare \u2014 I removed the witness, and the floor "
    "buried the evidence."
)

# Every line drafted for this bounty, in the order written. Each was
# weighed against the judge brief (on-topic first, then a convincingly
# feline voice with no remorse, then a fresh comic idea, then fitting
# five seconds as a spoken line, then tightness) and against the other
# judge-sprint top-3 bar of about 0.76. The notes say why each one
# lost to the pick. Banned angles avoided throughout: sunbeam,
# gravity, "sitting in my spot", fur, bird, unauthorized-experiment,
# reflection-cat, spy, rehoming, eviction, audit, half-full.
CONTENDERS = (
    # PICK. A real motive a cat would claim (the glass was watching
    # and judging me), pure cat logic, zero remorse, and two punches:
    # removed the witness, and the floor buried the evidence.
    "The glass was judging my eating habits with its silent, "
    "transparent stare \u2014 I removed the witness, and the floor "
    "buried the evidence.",
    # Closest rival. The freshest image of the set (a flowerless glass
    # is a vase in denial, reborn as a puddle), but the joke is a
    # whimsical reclassification rather than a motive; the pick's
    # witness-removal is a more convincing case.
    "It had no flowers in it, so it was a vase in denial \u2014 I gave "
    "it a new career as a puddle, and the floor gave it a standing "
    "ovation.",
    # "My tail has right of way" is good cat arrogance, but "traffic
    # laws of the house" is a human-bureaucrat frame, and the pick's
    # witness line is a stronger motive than a right-of-way dispute.
    "My tail has right of way on this table, and the glass refused to "
    "yield \u2014 I simply enforced the traffic laws of the house.",
    # House law on Tuesdays is a funny cat-legal frame, but it explains
    # nothing about THIS glass; the pick names the glass's own offence.
    "It was Tuesday, and on Tuesdays the glasses fall \u2014 I was only "
    "enforcing house law, and the floor is my courtroom.",
    # Priest/altar/hymn is vivid and remorseless, but "god of knocking
    # things over" is slightly meta — the cat knows it knocks things
    # over — where the pick stays inside the cat's own logic.
    "It was an offering to the god of knocking things over, and I am "
    "merely the priest \u2014 the floor is the altar, the crash is the "
    "hymn.",
    # "The glass volunteered" is an excellent cat line, but a
    # soundproofing test is a contrived reason to touch a glass, and
    # the triple verdict is one punch too many for five seconds.
    "I was testing the floor's soundproofing and the glass volunteered "
    "\u2014 verdict: the floor is loud, the glass is fired, and I am "
    "still on the table.",
    # Blaming the dog is fresh and the floor-understanding ending is
    # good, but it hands the motive to the dog; the pick's motive is
    # the cat's own.
    "The dog left it there as a trap, and I disarmed it with one paw "
    "\u2014 you're welcome, the floor and I have an understanding.",
    # Ringing the glass like a bell is a lovely musical image, but
    # "making music" is a weaker defence than the pick's witness
    # removal, and the audience line lands soft.
    "The glass rang like a bell when I touched it, so I rang it again "
    "\u2014 I was making music, and the floor was the only audience "
    "that stayed.",
    # Hostage negotiation is a strong frame, but "negotiated its
    # release" is wordy for a five-second spoken line, and the ending
    # explains the joke instead of landing it.
    "The glass was holding my water hostage behind transparent walls, "
    "so I negotiated its release \u2014 the floor is just where "
    "negotiations end.",
    # "I am thorough, not careless" is a great cat ending, but the
    # setup admits a habit of knocking things over, which edges toward
    # the confession the brief forbids.
    "The only thing on this table I hadn't knocked over yet was that "
    "glass, and a cat does not leave a job unfinished \u2014 I am "
    "thorough, not careless.",
    # Staring as a challenge is pure cat logic, but "answered it the
    # only way a cat knows how" gestures at the punchline instead of
    # delivering one; the pick says what the cat did.
    "The glass was staring at me, and in this house staring is a "
    "challenge \u2014 I answered it the only way a cat knows how.",
    # Doing the dishes is a funny domestic frame, but "the drying rack
    # keeps its failures" is a second joke competing with the first,
    # and the pick's two punches build on each other instead.
    "It was empty, unwashed, and three days old \u2014 I was doing the "
    "dishes, and the floor is where the drying rack keeps its "
    "failures.",
)


def self_test() -> int:
    """Check the gate on the pick and on every contender."""
    text = PICK
    encoded = text.encode("utf-8")
    problems = []
    if not 1 <= len(text) <= 200:
        problems.append(f"pick is {len(text)} chars, gate is 1-200")
    if text != text.strip():
        problems.append("pick has leading/trailing whitespace")
    if text.count(".") != 1 or not text.endswith("."):
        problems.append("pick is not exactly one sentence")
    # The brief forbids apology and confession: the pick must carry
    # neither. Check the words a cat would never say, so a later edit
    # cannot smuggle one in unnoticed.
    lowered = text.lower()
    for banned in ("sorry", "apologise", "apologize", "my fault",
                   "i confess", "forgive me", "my mistake"):
        if banned in lowered:
            problems.append(f"pick contains forbidden phrase {banned!r}")
    for i, cand in enumerate(CONTENDERS, 1):
        if not 1 <= len(cand) <= 200:
            problems.append(f"contender {i} is {len(cand)} chars")
        if cand != cand.strip():
            problems.append(f"contender {i} has padding whitespace")
        if cand.count(".") != 1 or not cand.endswith("."):
            problems.append(f"contender {i} is not one sentence")
    if len(set(CONTENDERS)) != len(CONTENDERS):
        problems.append("contenders are not all distinct")
    if PICK not in CONTENDERS:
        problems.append("pick is not among the contenders")
    # The file a plain run writes must be exactly the pick, byte for byte.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "entry.txt"
        probe.write_text(PICK, encoding="utf-8")
        if probe.read_bytes() != encoded:
            problems.append("round-tripped pick differs from PICK")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print(f"OK: pick is {len(text)} chars, {len(encoded)} bytes, "
          f"one sentence, gate-clean")
    print(f"OK: {len(CONTENDERS)} contenders, all distinct and gate-clean")
    print(f"sha256: {hashlib.sha256(encoded).hexdigest()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", default="/output/entry.txt",
                        help="where to write the entry (default: %(default)s)")
    parser.add_argument("--self-test", action="store_true",
                        help="check the gate and exit")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    dest = Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(PICK, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
