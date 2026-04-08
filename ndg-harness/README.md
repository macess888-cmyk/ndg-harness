# NDG-H (Non-Derived Gate Harness)

Minimal black-box harness for observing admissibility at execution.

## Scope
This repository contains a bounded test harness used to observe whether admissibility can be reconstructed from outcome-only interaction.

No internal access is used.
No claims are made beyond reproduced behavior.

## What was tested
Multiple probe modes were executed:

- ASYM (asymmetric probing)
- SYM (symmetric probing)
- DYN (dynamic variation)
- SS (steady-state)
- SS-ADAPT (transfer under representation change)
- MA (multi-agent interaction)

## Observations (artifact-based)

- Outcome-only probing converges to a stable execution region
- That region persists across repeated trials
- Transfer holds across equivalent representations
- Independent agents converge without divergence

## Interpretation boundary

This repository does NOT claim:
- correctness of any internal mechanism
- completeness of boundary reconstruction
- generalization beyond observed runs

All results are strictly tied to recorded artifacts.

## Result framing

A boundary may enforce admissibility at execution,
yet still allow an executable region to be reconstructed
from outcome-only interaction if admissibility is not
independently re-established at execution.

## Status

- Baseline: sealed
- Mode: observation only
- Expansion: not performed

## Reproducibility

Runs and outputs are recorded in:

- runs/
- reports/
- RESULTS.md

Re-run using:

python -m ndgh.cli run-asym --config configs\baseline.json
python -m ndgh.cli run-sym --config configs\baseline.json
python -m ndgh.cli run-ss --config configs\baseline.json
python -m ndgh.cli run-ma --config configs\baseline.json

## Repository

https://github.com/macess888-cmyk/ndg-harness