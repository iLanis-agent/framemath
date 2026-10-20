#!/usr/bin/env python3
# Frame Math oracle - mirrors engine.js with Fractions: frame time is 1000/fps as an exact Fraction, shares and leftovers are exact, slots are found by counting up until the slots cover the task, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

FPS = "the frame rate must be a whole number from 1 to 1000"
WORK = "the task time must be from 0.1 to 1000 ms with at most one decimal place"
def fps_(t):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}", t) or not 1 <= int(t) <= 1000: raise ValueError(FPS)
    return int(t)
def work_(t):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}(\.[0-9])?", t) or not F(t) >= F(1, 10) or not F(t) <= 1000: raise ValueError(WORK)
    return F(t)
def r2(fr):  # exact Fraction to text, 2 places half up, trailing zeros dropped
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 100); fs = str(fp).zfill(2).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def one(fr):
    t = fr * 10; assert t.denominator == 1
    ip, fp = divmod(int(t), 10); return f"{ip}.{fp}" if fp else str(ip)
def ms(f): return r2(F(1000, f)) + " ms"
def fr_(f): return "1 frame" if f == 1 else f"{f} frames"

def frame(a):
    f = fps_(a); return f"At {fr_(f)} a second, each frame lasts {ms(f)}."
def budget(a, b):
    f = fps_(a); w = work_(b); fm = F(1000, f); head = f"A task of {one(w)} ms "
    if w == fm: return head + f"uses all of a {ms(f)} frame, with nothing left."
    pct = r2(w / fm * 100)
    if w < fm: return head + f"uses {pct} percent of a {ms(f)} frame, which leaves {r2(fm - w)} ms."
    return head + f"uses {pct} percent of a {ms(f)} frame, which is {r2(w - fm)} ms over."
def slots(a, b):
    f = fps_(a); w = work_(b); fm = F(1000, f); n = 1
    while n * fm < w: n += 1
    return f"A task of {one(w)} ms needs {n} frame slot{'' if n == 1 else 's'} at {fr_(f)} a second, which is {r2(n * fm)} ms in all."

FNS = {"frameTruth": frame, "budgetTruth": budget, "slotsTruth": slots}

def cases():
    c = []
    for f in ["1", "2", "24", "25", "30", "48", "50", "60", "72", "90", "100", "120", "144", "165", "240", "333", "500", "999", "1000", " 60 "]: c.append(("frameTruth", [f]))
    works = ["0.1", "1", "4.2", "8", "10", "12.5", "16.6", "16.7", "16.67", "33.3", "40", "100", "999.9", "1000", "6.9"]
    for f in ["60", "30", "100", "144", "1", "1000", "24", "7"]:
        for w in works:
            if w == "16.67": continue
            c.append(("budgetTruth", [f, w])); c.append(("slotsTruth", [f, w]))
    for f, w in [("100", "10"), ("50", "20"), ("1000", "1"), ("250", "4"), ("125", "8"), ("200", "5"), ("60", " 16.6 "), ("3", "333.3"), ("3", "333.4"), ("3", "333.5")]:
        c.append(("budgetTruth", [f, w])); c.append(("slotsTruth", [f, w]))
    for v in ["", "x", "0", "1001", "1.5", "-1", "10000", "99999"]: c += [("frameTruth", [v]), ("budgetTruth", [v, "10"]), ("slotsTruth", [v, "10"])]
    for v in ["", "x", "0", "0.0", "0.05", "1000.1", "1.25", ".5", "5.", "-1", "10000", "1e3"]: c += [("budgetTruth", ["60", v]), ("slotsTruth", ["60", v])]
    r = random.Random(708)
    for _ in range(15):
        f = str(r.randint(1, 1000)); w = f"{r.randint(0, 999)}.{r.randint(0, 9)}"
        if w == "0.0": w = "0.1"
        c += [("frameTruth", [f]), ("budgetTruth", [f, w]), ("slotsTruth", [f, w])]
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":")) for o in out) + "\n]\n")
print(len(out), "cases written")
