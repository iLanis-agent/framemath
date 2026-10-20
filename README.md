# Frame Math

Frame time budget arithmetic. At 60 frames a second each frame lasts 16.67 ms, so a 12.5 ms task uses 75 percent of it and leaves 4.17 ms.

## What it computes

- **The frame truth** - the milliseconds in one frame at a frame rate (1 to 1000 frames a second).
- **The budget truth** - the share of one frame a task uses (0.1 to 1000 ms), and the milliseconds left or over.
- **The slots truth** - the whole frame slots the task needs, and the milliseconds those slots add up to.

## Boundary

Arithmetic only. It has not seen any app, screen or device. It does not know how long code really takes, how a display or browser schedules frames, or whether motion will look smooth, and it gives no verdict that a frame rate or a task time is good enough. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers, half-up rounding).
- `oracle.py` - the Python mirror (Fractions, counting slots up one at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (see the count it prints).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/framemath/
Repo: https://github.com/iLanis-agent/framemath
