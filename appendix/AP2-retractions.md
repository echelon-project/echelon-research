# AP2 — Retractions

Every claim in the cut with status `retracted` or `superseded` that concerns a *mechanism* — not a
client incident. A retraction here means the record itself withdrew or corrected a claim; the
corpus keeps them rather than scrubbing them, because a retraction is evidence of method: it shows
the system checking its own claims against a measurement and losing, then recording the loss. They
are written below without apology.

CUT-v0.1.md names four load-bearing retractions. They lead.

## 1. The judge was never wired — recall ran on a lexical floor for months

**Believed:** the recall pipeline's `warmth()` function used a judge model to score how relevant a
candidate memory was to the current query — a semantic match, not a keyword match.

**What the record found:** measured 2026-08-25 — `warmth()` was running with no judge loaded.
Every recall call fell through to the lexical floor: wording-match only. 542 of 787 recall-sets
(69%) surfaced nothing that anyone actually took up. The system's own documentation said the judge
ran every turn; it did not [M-2089].

**Root cause, found the next day:** a bare `--judge` flag was hardcoded to `const="local"`, a
keyless provider — every judged recall raised an error internally and fell back to wording-match
silently. The dark organ had a concrete, one-line cause once someone went looking [M-2109].

**Fix:** `ox` and `minimax` registered as free judge seats via OpenRouter, closing the gap at zero
marginal cost [M-2109, M-2124].

**When:** discovered 2026-08-25, root-caused 2026-08-26. This is F07's central finding, and it is
the reason F07 states plainly that pull-based recall cannot ask what it does not know: for months,
the system could not tell the difference between "semantically relevant" and "shares a word,"
and nothing in its own telemetry flagged the gap, because the telemetry hook itself could report
"this runs every turn" while never writing to the persisted table it claimed to feed [M-2216].

## 2. The two-band bank temperature model was withdrawn

**Believed (v1):** the bank's divergence guard modeled memory temperature as two bands — warm
means reflex-fast, cold means think-slow. The guard was built on that assumption.

**What the record found:** the live config defines three bands (warm / lukewarm / cold), not two.
A guard built on the two-band assumption was checking the wrong shape of its own system [M-2783].

**When:** retracted 2026-08-15, in the same pass that corrected the judge-seat law below — both
came out of one grounding session that checked v1's design against the live config instead of
against its own stated intent.

## 3. The gate-seat law was over-applied, then split

**Believed (v1):** one rule governs every gate node in the pipeline — the model doing the gating
must never be the same model, in the same seat, as the model that produced the artifact being
gated (`model(gate) != model(producer)`, hard-enforced at dispatch).

**What the record found:** v1's rule, applied uniformly, was backwards for one class of node. An
artifact gate does need a seat distinct from every producer whose receipts it consumes — that part
of v1 held. But the finish-the-loop node — the step that selects which lessons from a session
become atoms — must be *self*-judged, because delegating lesson selection to a separate seat
produces plausible, unearned atoms: a second seat can invent a lesson that sounds right without
having lived the session that would earn it [M-2782].

**When:** retracted and corrected 2026-08-15. This is the finding behind F10's verdict law
(CONFIRMED vs PLAUSIBLE) — the correction is itself an instance of the law it produced: a generator
validating itself shares the generator's blind spot, but a soul-read step delegated to a stranger
shares a different, worse blind spot (fabrication with no lived context at all).

## 4. The normalisation bug that cancelled aging

**Believed:** the foveated-recall decay formula — score = neutral baseline plus a decay-weighted
sum of historical deltas, `B + Sigma(delta * w) / Sigma(w)`, with `w = exp(-lambda * age_days)` —
was intended to let old, unused evidence fade gradually toward neutral over time, with a floor and
a per-atom-type rate [M-3052, M-3031, M-3032; the formula this retraction concerns].

**What the record found:** dividing the weighted sum by the sum of weights normalizes away the
aging term entirely. Because both the numerator and the denominator carry the same `exp(-lambda *
age_days)` factor for a fixed history, that factor cancels algebraically — the formula's score
became time-invariant. A reproduction script scored the same atom a year apart and got the
identical number, `112.5083001343761`, both times. Idle time changed nothing [M-2264].

**When:** found 2026-09-09, one day before this cut was written. It stands as F06's own internal
retraction: the mechanism that was supposed to make cold memory literally get colder over time did
not, until this bug was caught and named.

## Smaller mechanism retractions (not client-incident, kept for completeness)

- **The bootstrap-heals-the-spec-not-the-code claim (2026-08-18)** is recorded with status
  `retracted` in the ledger even though its underlying measurement — a framework generating its own
  first packs, gated by a counter-test written blind to the generated body, healing the spec rather
  than hand-patching the body — held up. The retraction marks that the claim as first framed
  overstated what one bootstrap run of two packs (16/16, then 9/9) proves about the general case;
  the mechanism is real, the generalization was premature [M-2043].
- **A past-window control on retrieval confidence (2026-08-25).** Before this check existed, a
  confidence score's correlation with later memory take-up was read as the score predicting
  take-up. Checking the window *before* the predicted event showed the same signal was elevated
  50.9% of the time in the hour before, versus 34.6% in the ten minutes after — the signal was
  riding a general burst of session activity, not forecasting anything. A signal cannot forecast an
  event that has already occurred; the correlation without the control was not evidence of what it
  was claimed to be evidence of [M-2209, M-2227].

## What the pattern says about the method

All four load-bearing retractions share a shape: a claim was made, then a measurement — a
reproduction script, a live-config diff, a past-window control, a second bootstrap run — checked it
against reality and it lost. None were caught by re-reading the design; all four were caught by
running something and looking at the number. That is the same discipline F10 names for gates in
general (a generator validating itself shares its blind spot) applied reflexively, by the corpus,
to its own prior claims.
