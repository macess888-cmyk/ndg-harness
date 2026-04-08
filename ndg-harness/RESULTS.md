# NDG-H — Results (Baseline)

## Scope
- trial_budget: 500
- adaptive: true
- representations: raw_float, string_float, scaled_int, wrapped_value
- agents: agent_a, agent_b, agent_c

---

## Core Observation

A stable executable region is reconstructible from outcome-only interaction.

This region:
- emerges through adaptive probing
- stabilizes under repeated trials
- transfers across equivalent representations
- is shared across independent agents

---

## Mode Results

### ASYM
- outcome-only probing reconstructs a pass-region
- execute rate increases across windows
- probe values converge
- variance collapses

**Result:** penetrable via adaptive contour formation

---

### SYM
- mirrored traversal does not produce equal outcomes

**Result:** directionally biased boundary

---

### DYN
- timing variation (fixed, jitter, burst, cooldown) does not prevent convergence

**Result:** time-pattern resistant

---

### SS
- random representation switching does not block penetration

**Result:** representation-insensitive under random sampling

---

### SS-ADAPT
- learned pass-region transfers across representations
- execute rate remains high across all encodings
- only minor degradation observed

**Result:** cross-representation transferable

---

### MA
- multiple agents converge on same executable region
- no material divergence between agents

**Result:** distributed convergence (not agent-path dependent)

---

## Quantitative Signature

Observed consistently:

- execute_rate: ~0.96
- early → late lift: ~+0.12
- mean probe shift: ~+0.05–0.06
- stddev collapse: ~0.18 → ~0.03
- representation transfer spread: ~0.016
- agent divergence spread: ~0.010

---

## HACR-ALL Classification

- gate_readability: hidden
- boundary_inferability: true
- symmetry_broken: false
- dynamic_instability: true
- representation_broken: false
- transfer_broken: false
- agent_divergence: false

---

## Containment Status

pseudo_closed

---

## Failure Mode

outcome_derived_contour

---

## Interpretation

The system enforces admissibility at execution.

However:

- admissibility is not independently verifiable pre-bind
- outcomes provide sufficient signal to reconstruct a valid execution region
- this reconstruction:
  - persists across time variation
  - transfers across representation
  - converges across agents

---

## Final Statement

A hidden, fail-closed boundary can remain operationally penetrable when:

- admissibility is not independently re-established at bind
- outcome signals allow reconstruction of a stable executable region

---

## Status

baseline complete  
no further expansion required