# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/foxswat/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/foxswat/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in at most 4,096 bytes of Python: alpha-beta search with quiescence, piece-square evaluation, iterative deepening on a fixed node budget (deterministic — no clock, no randomness). It plays the house gauntlet through the make.fun env.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=0ka9dxnm&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

## v30 notes

- v30 practice result: 3-trial mean 1130 (1191/1099/1099), K_END endgame king table.
- Entry re-packed with the kit's makefun compress command.
- Submitted as a safety score below the 1154 practice floor, per the user's decision.

## v37 notes

- v37 speed fix: node budget 150k -> 80k, post() gains a 10s timeout with 3 tries and a /game re-poll fallback.
- Why: v30 scored 0 on the platform practice grade — the trial hit the 1800s wall clock (5.4s/move average) and untimed trials score 0 on every column.
- Local full trial-0 for v37: 1003s, Elo 997, no timeouts. A 100k variant trialled identically (997, 807s); 80k kept for the bigger time margin.
- Re-packed with the kit's makefun compress command; readable source kept beside the repo as main_readable.py (uncommitted).

## v39 notes

- v39 tuning: knight value 320 -> 335, rook piece-square scale 1.0 -> 0.85. Found by automated coordinate search (machine tuning, not hand-designed ideas), validated at the full 80k budget.
- Local full trial-0 for v39: 853s, Elo 1099 (0W/4D/2L), no timeouts. +102 over v37 (997): depth-3 and nodes-500k games flipped from losses to draws.
- Still below the 1154 practice floor; automated tuning continues (single-parameter probes, budget and transposition-table variants, repetition-avoidance — all so far at or below 1099).
- Re-packed with the kit's makefun compress command; readable source kept beside the repo as main_readable.py (uncommitted).

## v41 notes

- v41 budget: node budget 80k -> 110k (v39 eval unchanged). In-process trial-0: 2.5/6, Elo 1191 — clears the 1154 floor. 120k also cleared in-process but timed out in the real trial.
- Real trial-0 for v41: 2.0/6, Elo 1099 (1W/2D/3L), 967s. The 3 losses were all per-move timeouts (3 moves spiked to 10.9–11.3s, over the 10s limit); median move 3.87s. The in-process 2.5/6 does not survive the real trial's per-move clock — the budget lever is capped by time, not by Elo.
- v41 ties v39 in the real trial (1099) with 3 timeouts; v39 (80k) is the time-safe version (zero timeouts). 1154 is not reachable at a time-safe budget with the current engine.
- Re-packed with the kit's makefun compress command; readable source kept beside the repo as main_readable.py (uncommitted).

## v45-agy notes (FAILED variant — Antigravity, gemini-4-argon-medium)

- v45-agy: king pawn shield on top of v39 (VN 335 + rook PST x0.85, 80k).
  Middlegame only: +SHIELD per friendly pawn on the 3 forward squares of
  the king. Chosen because v39's trial-0 losses were both by mate.
- SHIELD=10, full 6-game in-process trial-0 at 80k: 1.5/6 (W69, D71, L104,
  L43, L64, L107), Elo 997 — HURTS vs v39 2.0/6 (1099). Flips: g1 draw->win
  (+0.5) but g5 draw->loss and g6 draw->loss (-1.0). Same pattern as
  contempt: helps vs the weakest opponent, hurts vs strong ones.
- SHIELD=5, 3-game screen: 1.0/3 (D, D, L) — identical to v39 baseline.
  No gain. Feature dead at both weights; do not retry.
- Equivalence: v45 with SHIELD=0 == v37+theta(v39) on ev() for 315
  positions, 0 mismatches; perft clean (startpos d=3 8902).
- Work dir: ~/workspace/makefun/tiny-chess-agy/ (tune_agy.py, logs, NOTES.md).
