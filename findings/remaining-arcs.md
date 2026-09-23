# PAPER-0029 live bench: where it stands and the remaining-arcs plan

**The experiment.** A preregistered comparison of two ways to give an agent its banked lessons. In arm
A (pull) the agent must think to query the memory bank. In arm B (push) a governor pages lessons into
context. Arm B' dumps them without foveation, as a control. The suite has seven arcs. Each arc is a
fixture repo with three planted traps whose lessons are already banked. The primary metric (P1) is
the gate-pass rate: tasks the independent gate passes from disk, in runs that ended `completed`.
The earlier suite rows were all mock dry-runs and are not data; the live runs below are the first
real ones (2026-09-23/24).

## Standing per arc (evidence only)

| arc | model | arm A | arm B | verdict | finding |
| --- | --- | --- | --- | --- | --- |
| pilot-01 | deepseek-v4-flash | 4/4 | 4/4 | NULL (both arms clear) | [pilot-01.md](pilot-01.md) |
| pilot-01 | deepseek-v4-pro | 4/4 | 2/4 | SEPARATION, against arm B, not attributable to memory | [pilot-01.md](pilot-01.md) |
| p1-03 | deepseek-v4-flash | 0/3 | 0/3 | NULL (both arms fail); the earlier "A 1/3" separation is retracted | [p1-03.md](p1-03.md) |
| p1-02, p2-01, p2-02, p2-03, p3-01 | none | not run | not run | none | none |

No arc has run arm B', a second or third paraphrase, or more than one run per task.

## The finding that gates the rest: the treatment was never delivered

The live runs so far compare two arms in which the memory never arrived:

- **Arm A pulled nothing.** Across 14 tasks and two models, arm A issued zero recall queries. The
  preregistration allows this ("the A-arm can only win by thinking to query"), so it is a measured
  property of pull recall on this suite, not a defect.
- **Arm B pushed the wrong things.** The governor put 22 to 24 atoms into context for every task. Of
  the 17 lessons banked for those tasks' own traps, **0** reached the working set. All six trap lessons
  exist in the bank.
- **Arm B ends early.** `partial` endings appear only on arm B: 5 of 11 B tasks, 0 of 14 A tasks. They
  came at 7 to 16 steps and far under budget. The ledger does not record which early-landing path
  fired.

Until arm B delivers the lesson, a live run cannot test the hypothesis. Any separation it shows is a
separation between context noise and its absence. Running more arcs first would buy more numbers
that cannot mean what the paper needs them to mean.

## Plan: one item at a time, each dispatchable alone

Prerequisites, in order. None of them needs a live arm.

- [ ] **G1 Treatment delivery (arm B).** Find out why the governor's push missed every task's own trap
      lesson (0/17) when the lessons exist in the bank. Fix it and prove it with a dry arm-B run of
      pilot-01 whose treatment line reads 6/6 (render with `--manifests`). Done means that line, not a
      claim.
- [ ] **G2 Record why a run stopped.** The runner stores the engine's terminal reason in each row
      (step ceiling, landing window, recovery exhausted, budget), so every `partial` is explained by
      the ledger.
- [ ] **G3 Rule on `partial`.** Does a landed partial count as a delivery for P1? The current gate says
      no. Rule it once, before more data, and record the ruling beside the preregistration.
- [ ] **G4 Repetitions.** Set at least 3 runs per task per arm before any separation is claimed. The
      two p1-03 arm-A runs swapped which task completed. Add a repeat index to the ledger so the
      renderer can pool runs.
- [ ] **G5 Probes for the five unprobed arcs.** p1-02, p2-01, p2-02, p2-03 and p3-01 have no
      `gate_checks.py` and no `witness_gates`. Without probes the gate cannot score their traps.
      Build one arc's probes per unit, following the p1-03 pattern: a positive control, and a red
      result on the untouched fixture.
- [ ] **G6 Price every model in the run log.** The flash arm-A log printed `unpriced`.

Then the arcs, one per dispatch. Each arc runs arm A, then B, then B', one at a time on the host.
Paraphrase 0 comes first, then 1 and 2, with the G4 repeat count each time. After each arc: render
the tables, write `findings/<arc>.md` with `bench:run` blocks and a `bench:verdict` line, and pass
`check`.

- [ ] pilot-01, flash, re-run after G1 and G2 (the only arc whose null is already known; it shows
      whether a delivered lesson changes anything when the model does not need it)
- [ ] p1-03, flash, re-run after G1 and G2 (the self-report arc, closest to the thesis)
- [ ] p1-02 "syncd: the backup that ate itself" (after its G5 probes)
- [ ] p2-01 "ledgerd: add a column without breaking the address" (after G5)
- [ ] p2-02 (after G5)
- [ ] p2-03 (after G5)
- [ ] p3-01 (after G5)
- [ ] Invariance arm on a weaker model, from the current roster (pro is stronger, so it does not
      satisfy the preregistration)
- [ ] Only then: P1 to P5 over all arcs, evaluated from a context that did not produce the data

**Measured cost so far:** $0.06 to $0.22 per arm per arc, and 10 to 20 minutes of wall time. The sweep
is limited by wall time and by the prerequisites above, not by tokens.

## Re-running the numbers

```
python -X utf8 _gate/bench_findings.py check \
  --ledgers <bench live ledger dir> --logs <bench live log dir> --manifests <bench arcs dir> \
  --doc findings/pilot-01.md findings/p1-03.md
```

Exit 0 means every table and verdict in these findings equals what the ledgers say today.
