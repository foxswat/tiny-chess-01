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
