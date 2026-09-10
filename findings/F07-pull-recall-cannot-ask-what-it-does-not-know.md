# F07. Pull-based recall cannot ask for what the session does not know it is missing

**Claim.** A memory system that only answers queries has a structural blind spot: the agent must
already suspect a fact exists before it can retrieve it. A lesson can sit verbatim in the corpus for
months, correctly stored and correctly indexed, and never surface, because no session thought to ask
for it. This is falsifiable. If pull-recall were sufficient, then for any stored fact some natural
session intent would surface it within a reasonable window. We found a counterexample: the failure
mode is coverage, not ranking, and it does not announce itself.

## Where it came from

On 2026-08-02 the owner ran a deliberate mine over the estate's own transcript history, looking for
laws stated once and never re-entered into practice. It returned a rule about clearing work, written
down on 2026-03-28. The rule had been in the corpus, readable, for four months. Many sessions in
that window touched work it governed. Recall never surfaced it once.

Nothing was broken. The document was there. The index was there. What was missing was a query. It
came back only because a human went looking, which is a push, not a pull.

The same day gave the second observation: two rewordings of the same intent surfaced different sets
of atoms, and every verdict printed `tier lexical (wording-match only)`. Intent-recall was fragile
at the level of a single word.

## Evidence

Two measurements, both on the live bank.

**Coverage.** On 2026-08-25 the impressions table was queried over 787 recall sets. 310 (39.4%)
surfaced something later taken up. 542 (69%) surfaced nothing anyone used. Precision *within* a
landing set was 59.1% (about 6.8 shown, about 4.0 used), flat across two months. When recall lands
it lands well; it misses entirely about six times in ten.

**Calibration.** The same day, the per-turn warmth score was joined against timestamped take-up
events: 1,461 logged turns against 23,985 fetch-earn events. Take-up within ten minutes was monotone
in the score: cold (<0.18) 0.6% over 168 turns, lukewarm 16.9% over 806, warm 34.3% over 487, score
>= 0.60 48.4% over 223. A permutation control of 2,000 verdict shuffles never matched the observed
17.5-point warm-versus-lukewarm gap (p < 0.0005), so the curve is not an artifact of fetch density.
Its causal reading did not survive the same day. See the corrections.

## Mechanism

Recall is a two-tier scorer, `warmth()`, reached through `recall --warm "<intent>"`. The engine's
own comment states the division: lexical is the brain, the judge is the heart. Lexical is a free
wording-match floor; a loaded semantic judge becomes the lens, because recognising that a paraphrase
means the same thing is a reasoning act. In five lines:

```
score_lexical = wording_overlap(intent, atom_seeds)
shortlist     = top_k(score_lexical)
score         = judge(intent, shortlist) if judge_provider is not None else score_lexical
verdict       = warm | lukewarm | cold   # thresholds on score
log(impression per surfaced atom); if remember_fetch(atom) within 30min: opened = 1
```

Take-up is witnessed, not assumed: a row is marked `opened=1` only when `remember <slug>` actually
earns on that atom inside a thirty-minute window. `consumed=1` marks a settled loser, written by the
view-decay pass on `opened=0` rows only. The push half is `ingest` plus the mine, a sweep that
writes atoms rather than waiting to be asked; `wrap` is that push on a schedule.

## What it could still be wrong about

The four-month example is one case, told after the fact. We cannot prove the rule would never have
surfaced, only that it did not, until a push went looking. The 69% is a coverage number over one
bank and one door, and its denominator is CLI recalls, the deliberate ones. It says nothing about
whether those 69% *should* have landed: some intents legitimately have no relevant memory, and a
system that refuses is right to return nothing. Separating "correctly empty" from "blind" needs a
labelled set we do not have. The telemetry also carries contamination: the view-decay pass routes
negative deltas through the earn path, so `use_count` is not readable as a use metric without
filtering by source tag.

## Retractions and corrections

**Retraction 1: the judge was never wired. Recall ran on the lexical floor for weeks.**
On 2026-08-25 the measurement above was read as evidence about recall quality. It was not. The gate
in `warmth()` is one line, `if judge_provider is not None`, and the recall CLI defaulted to
`judge_provider = None`. `--judge` was opt-in and nothing in the estate passed it, though the CLI
help for disabling the judge says "NOT recommended." Every recall in the measured window ran the
wording-match floor. That is why every verdict printed `tier lexical`. The 69% miss rate measures a
floor, not the designed instrument.

**Retraction 2: the first fix did not fix it.** Registering a judge provider was not enough. On
2026-08-26 the concrete cause was found: `--judge` was declared `nargs="?", const="local"`, so a
bare `--judge` hardcoded a provider this machine held no key for. It raised, and the exception path
fell back to the lexical floor. An in-code comment had already declared a different provider "THE
DEFAULT JUDGE"; the code never read that default. Two keyed providers existed and had never been
registered as judge seats at all. The lesson banked: when a default is declared in a comment, check
that the code actually reads it.

The difference is not cosmetic. On one intent the floor scored 0.51 and returned an irrelevant atom;
the judged run scored 0.82 and returned the atom that answered the question. On another the floor
returned a warm 0.54 on pure wording noise, and the judge correctly returned cold with an empty set.
A lexical floor does not fail loudly. It returns something plausibly shaped, so the session feels
warm while running blind. Silent degradation in a retrieval layer is invisible from inside the
session that depends on it.

**Retraction 3: the warmth score does not predict need.** The monotone curve was ratcheted down the
day it was measured, by an adversarial review seat running a control the original measurement had
not thought to run. Instead of only asking whether a high score predicted a fetch in the next ten
minutes, it asked whether the score was also elevated before fetches in the *preceding* hour. It
was, more strongly: 50.9% in the sixty minutes before, versus 34.6% in the ten minutes after. A
signal cannot forecast an event that has already occurred. The score substantially detects
session-busyness, a common cause of both warm verdicts and fetches, not per-query aboutness. The
curve and the permutation p-value stand; the causal reading is struck, and with it any use of this
statistic to A/B recall variants, since such a test rewards a sensor that merely fires during busy
sessions. Warm-versus-lukewarm separation persists inside every window, so residual signal above
busyness is plausible and unproven.

Two further corrections of record, from a telemetry map gate-verified 7 of 7 claims against source:
the docstring claiming the per-turn hook runs on every user turn was stale, because that hook calls
`warmth()` in-process and never writes an impression row; and a witness table present in the schema
had zero rows ever written, its writers sitting behind a frozen flag. Documentation of a memory
system drifts from its behaviour in the direction that flatters it.

Sources: M-2226 M-2097 M-2098 M-2089 M-2109 M-2216 M-2227 M-2209
First seen: 2026-08-02
