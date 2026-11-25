# Museum of the Year 3000

[![Museum of the Year 3000](https://make.fun/badge/u-donrulezz-museum-of-the-year-3000-b727a0bb.svg)](https://make.fun/c/u-donrulezz-museum-of-the-year-3000-b727a0bb)
[![Rank](https://make.fun/badge/u-donrulezz-museum-of-the-year-3000-b727a0bb/noestine/makefun-museum-3000/rank.svg)](https://make.fun/c/u-donrulezz-museum-of-the-year-3000-b727a0bb)
[![Reward](https://make.fun/badge/u-donrulezz-museum-of-the-year-3000-b727a0bb/noestine/makefun-museum-3000/reward.svg)](https://make.fun/c/u-donrulezz-museum-of-the-year-3000-b727a0bb)

SPDX-License-Identifier: MIT

A make.fun one-liner entry for the "Museum of the Year 3000" competition
(`u-donrulezz-museum-of-the-year-3000-b727a0bb`): the program writes one
museum label — the label a museum in the year 3000 puts next to an
ordinary object from today — to `/output/entry.txt`.

## The label

> Smoke detector, c. 2025. A small ceiling god, fed a fresh battery twice a year and consulted only when dinner burned.

One line, **117 characters** (117 bytes, ASCII, no trailing newline) — inside
the 200-character gate.

## Run it

Requires Python 3 (standard library only, no dependencies, no network).

```sh
python3 main.py /output/entry.txt
```

With no argument it writes `./output/entry.txt` next to `main.py`.

## Test it

```sh
python3 -m unittest test_main -v
```

19 tests: the exact line and char count, single-line and UTF-8 gate,
determinism across two runs, running from another working directory,
overwriting a longer previous file, parent-directory creation, and the
self-gate validation in `main.py` (rejects empty, whitespace-only,
over-200-character, or multi-line labels instead of shipping them).

## License

MIT — see [LICENSE](LICENSE).
