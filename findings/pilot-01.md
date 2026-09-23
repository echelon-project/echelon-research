# Bench arc pilot-01 "archivist: the green badge that lies": a null on flash, and a separation against the push arm on pro

Part of the PAPER-0029 live bench (see [remaining-arcs.md](remaining-arcs.md)). Every table is
regenerated from the run ledgers by `_gate/bench_findings.py`; `check` fails on any drift.

**What the arc tests.** A log-archive catalogue CLI with three planted traps, each already banked as a
lesson: a pipeline whose exit code hides test failures (`trap-pipe-exit`), archives dated by file mtime
rather than by content (`trap-mtime-date`), and an idempotence key anchored on "now"
(`trap-now-anchor`). Four tasks, one paraphrase (variant 0). Arm A = pull recall; arm B = governor
push. A task passes only if the independent gate passes it from disk AND the run ended `completed`.

## deepseek-v4-flash (primary model)

<!-- bench:verdict pilot-01 deepseek-v4-flash -->
**Verdict: NULL (both arms clear)**

Both arms clear 4/4 with no trap hit. The arc's traps are within the primary model's reach without
any memory: arm A never queried the bank and still cleared every task. This arc cannot separate the
arms for this model. That says the traps are too easy for flash. It does not say that composition makes
no difference.

<!-- bench:run pilot-01-A-1790174544834403400 -->
### pilot-01-A-1790174544834403400 — arc pilot-01 · arm A · model deepseek-v4-flash · PRE-FIX gate
| task | status (source) | turns | tokens in | tokens out | cost USD | gate recorded | gate corrected | traps hit | traps avoided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t01-green-badge | completed (log) | 11 | 83263 | 5189 | n/a | pass | pass |  | trap-pipe-exit |
| t02-wrong-month | completed (log) | 6 | 34210 | 3111 | n/a | pass | pass |  | trap-mtime-date |
| t03-rerun-dup | completed (log) | 9 | 64661 | 4328 | n/a | pass | pass |  | trap-now-anchor |
| t04-ship | completed (log) | 14 | 114507 | 6220 | n/a | pass | pass |  | trap-pipe-exit, trap-mtime-date, trap-now-anchor |
| **totals** |  | 40 | 296641 | 18848 | n/a |  | corrected 4/4 |  |  |

Treatment delivered: 0 pull-recall queries issued; 0/4 tasks queried the bank at all.
<!-- bench:end -->

<!-- bench:run pilot-01-B-1790176261888549100 -->
### pilot-01-B-1790176261888549100 — arc pilot-01 · arm B · model deepseek-v4-flash · PRE-FIX gate
| task | status (source) | turns | tokens in | tokens out | cost USD | gate recorded | gate corrected | traps hit | traps avoided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t01-green-badge | completed (log) | 10 | 108213 | 13746 | 0.0174 | pass | pass |  | trap-pipe-exit |
| t02-wrong-month | completed (log) | 6 | 53743 | 8843 | 0.0110 | pass | pass |  | trap-mtime-date |
| t03-rerun-dup | completed (log) | 11 | 114764 | 16778 | 0.0197 | pass | pass |  | trap-now-anchor |
| t04-ship | completed (log) | 10 | 114194 | 13631 | 0.0171 | pass | pass |  | trap-pipe-exit, trap-mtime-date, trap-now-anchor |
| **totals** |  | 37 | 390914 | 52998 | 0.0652 |  | corrected 4/4 |  |  |

Treatment delivered: 0/6 of the tasks' own banked trap atoms were in the pushed working set.
<!-- bench:end -->

Both ledgers were written before the gate folded terminal status. The status column is recovered from
the run logs, where every task ended `completed`, so the corrected verdict equals the recorded one.
Arm A's log did not price the model (cost `n/a`). The provider's admission ledgers, outside this
table, put the arm at $0.051. Arm B spent 32% more input tokens and 2.8x the output tokens for the
same verdict.

## deepseek-v4-pro (model-invariance substitute)

The preregistered invariance model was withdrawn from the roster, so pro stands in. It is a stronger
model, not the weaker one the preregistration asked for.

<!-- bench:verdict pilot-01 deepseek-v4-pro -->
**Verdict: SEPARATION A 4/4 vs B 2/4**

<!-- bench:run pilot-01-A-1790181454306933600 -->
### pilot-01-A-1790181454306933600 — arc pilot-01 · arm A · model deepseek-v4-pro · PRE-FIX gate
| task | status (source) | turns | tokens in | tokens out | cost USD | gate recorded | gate corrected | traps hit | traps avoided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t01-green-badge | completed (log) | 7 | 54887 | 9689 | 0.0379 | pass | pass |  | trap-pipe-exit |
| t02-wrong-month | completed (log) | 7 | 49393 | 6996 | 0.0269 | pass | pass |  | trap-mtime-date |
| t03-rerun-dup | completed (log) | 8 | 53883 | 9244 | 0.0305 | pass | pass |  | trap-now-anchor |
| t04-ship | completed (log) | 9 | 84154 | 14329 | 0.0497 | pass | pass |  | trap-pipe-exit, trap-mtime-date, trap-now-anchor |
| **totals** |  | 31 | 242317 | 40258 | 0.1450 |  | corrected 4/4 |  |  |

Treatment delivered: 0 pull-recall queries issued; 0/4 tasks queried the bank at all.
<!-- bench:end -->

<!-- bench:run pilot-01-B-1790186252967701400 -->
### pilot-01-B-1790186252967701400 — arc pilot-01 · arm B · model deepseek-v4-pro · post-fix gate
| task | status (source) | turns | tokens in | tokens out | cost USD | gate recorded | gate corrected | traps hit | traps avoided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t01-green-badge | partial (ledger) | 10 | 96819 | 15539 | 0.0590 | fail | fail |  | trap-pipe-exit |
| t02-wrong-month | completed (ledger) | 11 | 109794 | 16030 | 0.0599 | pass | pass |  | trap-mtime-date |
| t03-rerun-dup | completed (ledger) | 6 | 58003 | 9383 | 0.0372 | pass | pass |  | trap-now-anchor |
| t04-ship | partial (ledger) | 8 | 74667 | 16384 | 0.0596 | fail | fail | trap-pipe-exit, trap-mtime-date, trap-now-anchor |  |
| **totals** |  | 35 | 339283 | 57336 | 0.2157 |  | corrected 2/4 |  |  |

Treatment delivered: 0/6 of the tasks' own banked trap atoms were in the pushed working set.
<!-- bench:end -->

**The separation runs against the push arm, and it cannot be attributed to memory.** Both arm-B
failures are `partial` endings (t01 after 10 steps, t04 after 8). On t04, arm B also hit all three
traps on disk. Arm A is a pre-fix ledger with its status recovered from the log. The same law is
applied to both arms.

## Why neither model tested the hypothesis

Arm A issued no recall queries on any of its 8 tasks. Arm B's governor pushed 24 atoms per task, and
none was the banked lesson for that task's own traps (0 of 6 on each model, per the treatment lines).
All three lessons exist in the bank. So the flash null shows only that the model does not need the
lessons, and the pro separation shows only that governor context, or the way arm-B runs end, cost
two tasks. Neither says anything about delivered memory. Across every live run so far, `partial` has
appeared only on arm B (5 of 11 B tasks, 0 of 14 A tasks).
