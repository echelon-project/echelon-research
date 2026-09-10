# Recall is foveated, and forgetting is demotion rather than deletion

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

## Claim

A memory substrate that grows past the context window does not need a delete policy. It needs an
eye. Recall should behave like foveated vision: records matching the current intent come into sharp
focus and enter the context, the rest stay dormant in the periphery, still stored and queryable.
Forgetting is then a ranking effect, not a data operation. A record that draws negative signal, a
human dispute or a run of losses to a sibling in the same result set, loses weight and drops out of
the default view; one that pays off again comes back on its own. The stronger version of that
sentence, that a record fades on idleness alone, is retracted below: the formula as shipped cancels
common aging, so only an explicit signal moved a score.
Records here are atoms, one lesson per file, stored in the bank, the on-disk store that outlives any
one session. Weight is that atom's stored selection score, and warmth is the per-query relevance
number recall computes against the current intent. Falsifiable two ways. First, no code path may
delete a record. Second, dormancy must be reversible with no special verb: take a record below the
threshold, use it successfully once through the witnessed door, meaning `remember`, the engine verb
that returns a body and logs the read, and it must reappear in normal recall. If waking it needs a manual undelete or a batch job, the model is
deletion wearing a softer word.

## Where it came from

2026-07-30. The owner asked a question about his own system he could not answer: *"on the note on
decay, i notice even i didn't know. when the decay law fires?"* A forensic pass was commissioned
that hour to find out whether the substrate had a forgetting law at all. In the same conversation
he gave the shape he wanted: *"earn on satisfied use, decay on being passed over, rate set by how
perishable the atom type is"*, and the rule that has stood since, *"demote don't delete"*.

He also gave the analogy the implementation followed, mapping search engine ranking onto the two
recall verbs: *"view are like recall / opening link are like remember"*. Shown but not clicked is a
weak negative signal; clicked is positive. That is why the substrate logs impressions. The foveation
half was older, stated in the boot banner as one of four standing claims: *"Recall is FOVEATED
VISION. The warmth BANK is an eye: atoms matching your current intent come into sharp focus, the
rest stay dormant-but-active in the periphery."*

## Evidence

The audit came back blunt: *"A time-decay formula EXISTS and is correctly implemented, but it fires
ONLY on mutation ... There is NO automatic 'forgetting'."* On deletion it was equally direct after
searching the store: no DELETE statements anywhere, and the comment in the sleep organ, the background pass that proposes
housekeeping, reads *"nothing is
ever DELETED, pruning here means PROPOSE-for-prune; a weak atom is reported, not removed."* The work
of 2026-07-31 closed the first gap.

The fixes were measured on a copy of the live bank, 1073 records. Moving decay to read time made
aging visible where it had been frozen: one record read *stored=75.00, recomputed=72.19*, while
recently touched records showed roughly zero difference. A test confirmed one history under a slow
and a fast rate gives different scores, the slow-decaying type higher.

The dormancy threshold was picked against a histogram of 7497 records taken the same day: 7353 at or
just above neutral, 112 at the disclaimed floor, one near the view-decay floor. It was set at 80,
between the disclaim floor of 75 and the view-decay floor of 85, so being passed over in search
results can never on its own hide a record. Disclaimed and disputed are one state under two names:
a human has explicitly marked the record wrong through the dispute verb, which pins its score to 75.
The dry run said 97 would be dormant that day, all in that state. Auto-wake was proven rather than asserted: a test takes a record at 79,
dormant and hidden, runs one witnessed read, and the recomputed score is 90.6, live again, *"No
extra verb needed."* The earning constant is small: the same report states a fetch is worth `+2`,
enough on its own to lift 79 to 81 and cross back. The 90.6 figure is larger than `+2` because the
score is a weighted mean, not a sum, so how far one read moves a record depends on how many prior
deltas it is averaged against. That history depth is not recorded in the source. For a two-entry
history it is arithmetic: with the neutral baseline at 100, a score of 79 means the weighted mean of
the deltas is -21, and adding a fresh `+2` at full weight against one prior delta of -21 aged to
weight 0.98 gives 100 + (-21 x 0.98 + 2) / (0.98 + 1) = 90.6. On a deep history the same read moves
the score much less. A reader rebuilding this should take the constant, not the headline number, as
the specification.

The middle band has its own measurement. Warmth runs on a 0 to 1 scale, separate from the 0 to 100 score, and is banded three ways: warm at
0.45 and above, lukewarm from 0.18, cold below. The two scales never mix. Warmth ranks a result for
one query; the score decides whether the record is in the default view at all.
On 2026-08-15 a design document recalled at lukewarm 0.383, and the guidance returned was *"CHECK,
partial recognition; look at the warmest seed, you may be near a known path."* The document followed
it, read two records through the witnessed door, and found four places where it had reinvented
existing organs: *"One recall returning lukewarm 0.383 and two witnessed remember calls corrected
all four."* One incident, not a rate, and the strongest evidence the middle band has.

## Mechanism

1. `recall --warm "<intent>"` scores every record against the intent and returns the top few with a
   band: warm above 0.45 is ground that paid off, lukewarm 0.18 to 0.45 means check the warmest one
   before exploring, cold below 0.18 is new ground. Every record shown is logged as an impression,
   a row recording that this record was displayed for this query hash. That is the view.
2. `remember <slug>` is the only door returning a record's full body, and each witnessed fetch
   through it appends a positive delta of `+2` to that record's history. A plain file read outside
   the door is not witnessed and earns nothing. That is the click.
3. Score is never stored pre-decayed. At read time it is recomputed from the append-only history as
   `score = 100 + sum(delta * w) / sum(w)`, `w = exp(-lambda * age_days)`, intended so that old
   evidence weighs less than new with no batch job. That intent does not hold: dividing by `sum(w)`
   cancels the aging term whenever the deltas age together, which the Retractions section below
   reproduces. As shipped, this line computes a time-invariant weighted mean of the deltas.
4. `lambda` is per record type: owner feedback 0.005 per day, reference material 0.04. One global
   constant either over-decays the valuable kind or under-decays the cheap kind.
5. Dormant is a computed predicate, `score < 80`, evaluated during the query. Recall filters those
   out by default, prints the count, and `--include-dormant` shows them tagged. A pass at `wrap`,
   the ritual that closes a session, charges records that kept losing to a sibling in the same query
   set, capped at three points, floored at 85, skipping feedback and owner-sourced types.

6. Those two constants do not meet. If the demotion pass cannot take a record below 85, and dormant
   is `score < 80`, then that pass can never make a record dormant by itself. Combined with the
   cancelled aging term, no automatic path to dormancy survives: the only route left is an explicit
   human dispute, which pins the score to 75. The dry run confirms it. All 97 hidden records were in
   that state, none arrived there by decay or by losing impressions. The floor was written as a
   safety rail; what it also does is close the last automatic door into the state this finding is
   about.

Nothing there removes a row. Waking is the same read path running again.

## What it could still be wrong about

The evidence is for the plumbing, not the outcome. Nothing is deleted, dormancy is computed, one
read wakes a record. It is not proven the resulting ranking beats a simpler policy such as plain
recency, or no decay at all. There is no A/B measurement of retrieval quality, and the constants,
0.02 default rate, 80 threshold, 85 floor, 10 losing impressions per point, were reasoned from a
histogram, not tuned against outcomes. The dry run is weaker than it looks: all 97 hidden
records had been explicitly disputed by a human, so the time-decay path to dormancy was never
exercised. A later review raised the sharper worry, that hiding is only honest if a hidden record
stays reachable when nothing better exists, because *"a hidden atom that can never be reached is a
deletion by another name."* No test enforces that.

The sharpest form of that worry is a loop in the signals themselves, and nothing above addresses it.
An impression is only logged for a record that was shown, and a record is only shown if it already
clears the threshold and ranks near the top. A record that drifts just under 80 therefore stops
accruing impressions at all, so it becomes eligible for neither the negative signal nor the positive
one, and its score freezes at whatever value hid it. "Waking is the same read path running again" is
then true only for an operator who already knows the slug and calls `remember` on it directly. For
anyone arriving through `recall`, the periphery is not dormant-but-active, it is unreachable by
default, and the second falsification condition is met only on a reading of "special verb" that
permits prior knowledge of the slug. Nothing in the record tests this, and the paragraph above is
argument, not measurement.

## Retractions / corrections

The decay function was wrong for about six weeks. The error was found on 2026-09-09 by a review that
reproduced it rather than read it. Dividing summed weighted deltas by summed weights cancels the
aging term whenever the deltas age together, the normal case: *"Sigma(delta*w)/Sigma(w) cancels any
common aging. Idle time never changes a score."* The reproduction fixed a history and computed the
score at two timestamps a year apart, getting the identical value `112.5083001343761` both times.

So the read-time recomputation was real and per-type rates did separate the types, but the promise
that an unused record fades toward neutral did not hold. Records only moved when something acted on
them. In practice demote-don't-delete ran on explicit negative signal, a dispute or a losing
impression, not on the passage of time, which is exactly what the 2026-07-31 report believed it had
fixed. The proposed correction is one constant in the denominator, `sum(w) + kappa`, letting a score
slide toward neutral as evidence ages without idleness pushing it below neutral. It was still a
recommendation, not a merge, at the time of writing.

Sources (release ledger ids): M-3191 M-3124 M-2526 M-2208 M-3053 M-3008 M-3031 M-3032 M-3052 M-2264
First seen: 2026-06-23
