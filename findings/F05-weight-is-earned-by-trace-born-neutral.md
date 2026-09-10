# Weight is earned by trace: an atom is born neutral and gains rank only when work that used it succeeded

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

## Claim

A stored lesson must not be allowed to declare its own importance. In ECHELON every atom is created
at a neutral score, and its rank rises only through a witnessed event: a fetch through the engine's
own door (a *receipt*: a logged act the engine performed, carrying ids and re-runnable), or the
success of a card (an ordered sequence of atoms that composes a procedure) that
loaded it. Nothing grades its own homework. The falsifiable part is narrow and testable: plant an
atom, do not use it, and its rank must be indistinguishable from every other unused atom no matter
how confidently its body is written. Read its file with `cat` instead of `remember` and its score
must not move. If a system lets the author of a memory set that memory's weight at write time, the
ranking degrades into a record of how emphatic the writer was.

## Where it came from

The rule was in place before it was written down. Its earliest dated statement in the archive is
2026-06-16, in the note on the `add_atom` read-flip: "Born neutral — NO score asserted." By
2026-06-23 it had become one of the four claims printed at the top of every project's memory banner,
in the same words used ever since. The pressure that produced it is ordinary. When a model writes
its own lessons at the end of a session, it writes them while still holding the feeling of the
session. Everything it just fixed feels important. If that feeling is allowed to set a number, then
six months later recall is ordered by yesterday's mood rather than by what actually worked. The
owner's fix was to remove the author's vote entirely. You may write the lesson. You may not score
it.

## Evidence

The witnessed line is this finding's own falsification test, run against the live engine on
2026-09-10 on a throwaway scope. Verbatim output:

```
[PASS] INGEST  planted 1 atom
[PASS] COMPILE earned_before={'score': 100.0, 'use_count': 0}
[PASS] RECALL  verdict=warm score=1.0; surfaced=YES        <- the peek did not move the score
[PASS] EARN    served=yes  score 100.0 -> 102.0  use_count 0 -> 1  MOVED=YES   <- one witnessed fetch
```

Read the four lines in order. A freshly planted atom sits at 100.0 with a use count of zero: born
neutral, at a value its author passed no argument for. A warm recall surfaced it and left the score
at 100.0, so browsing is genuinely free. One fetch through the engine's own door moved it to 102.0
and the use count to one. The upward move required an event the engine itself performed. That is the
property the claim asserts, observed rather than quoted from a docstring.

The constants behind that arithmetic are readable in the engine's earn-law module, also on
2026-09-10: a witnessed fetch adds 2.0, a hand-lowering subtracts 10.0, and the score floor is 1.0,
which decay approaches and never crosses, so nothing is ever scored out of existence.

The born value is 100.0 flat on the engine's internal scale. The 0.31 that appears in one node
specification is a normalised readout of the same neutral value, not a second law. What matters is
the property both express: the born value is identical for every atom and the author does not
choose it.

The read path splits into free and paid. `recall_peek()` is documented as "FREE peek — the spine
only. NO body, NO mutation. recall is free; fetch is what earns." `remember_fetch()` is documented
as "THE WITNESSED DOOR. Serve the structured fields and EARN BY DEFAULT (mechanical, no outcome
gate, no self-report — the fetch IS the witness)." Browsing is free, consuming is paid. The
operating law given to every agent follows from this: "Read a full atom via `remember <slug>`, never
`cat` the `.md` (a file-read is out-of-band; the bank never witnesses it)." An agent that reads the
file directly gets the content and gives the bank nothing.

The failure is dated 2026-09-08 and is the most useful evidence here. A review of the scoring
implementation found that "a fetch through `remember_fetch` stores `score += 2`", and ruled that
this is wrong: the fetch is a tenure event, not a quality verdict, and "storing fetch as a score
delta lets fetch count masquerade as outcome evidence." In other words, the mechanism designed to
stop an atom asserting its own significance had quietly acquired a second way for popularity to look
like correctness. An atom fetched forty times by habit outranked an atom fetched twice on jobs that
succeeded.

Say both halves of the current state. That review is a ruling against the fetch constant, and the
constant is still live: the selftest above shows a bare fetch moving the score by exactly the 2.0
the ruling condemned. The law was ratified and the implementation it condemns has not been changed.
So the selftest proves that a fetch is witnessed and that no author sets the score. It does not
prove that fetch has been separated from outcome, because on 2026-09-10 it had not been.

## Mechanism

Five lines, minus the storage details:

```
add_atom(body)          -> row with score = BORN, use_count = 0        # author sets no score
recall_peek(id)         -> spine only; no write                        # free
remember_fetch(id)      -> body + record a fetch event                 # witnessed, tenure
card_success(card_id)   -> for each atom the card loaded: credit it    # the real earn
fire_lower(id, reason)  -> decay toward the anchor; never delete       # the only hand-path down
```

`fire_lower` is the *hand-path*: the one place where a reader moves a score by hand rather than the
engine moving it by observing an event. The *anchor* it decays toward is the born value, 100.0. The
asymmetry is deliberate. There is no `fire_higher`. A reader who was misled by an atom has a
duty to push it down by hand; a reader who found an atom useful has no hand-path to push it up,
because that would be self-report again. Upward movement comes only from a card that finished.
Downward movement decays toward a neutral anchor and stops there. Nothing is deleted; a low-scored
atom is dormant, not gone, and still surfaces when a query matches it closely enough. The engine
verbs are `ingest` (plant), `recall --warm` (free), `remember` (paid), and `wrap` (which composes
the session's card, and so is where credit actually flows back).

## What it could still be wrong about

The strongest objection is that the split between fetch and outcome is easier to state than to
implement, and the archive shows it was implemented wrong for an unknown period. If fetch adds
score, then earn-by-trace has already collapsed into earn-by-attention, and the property being
claimed here was aspirational rather than live during that window. The correction is dated but its
merge is not confirmed in the material available, so the honest position is that the law was ratified
and the implementation was found in breach. Second, credit from a successful card is split across
every atom the card loaded, which rewards atoms that happened to be adjacent to a win. Over enough
runs that should wash out; there is no measurement in the archive showing that it does. Third, born
neutrality only removes the author's vote at creation. An author who wants an atom to rank can still
write it to match the phrasings they expect to query with, which is self-assertion moved from the
score field into the body. Rank at retrieval is a function of query match as well as stored score,
so the author also controls how many atoms exist on a topic: ten near-duplicates occupy ten slots in
any shortlist, which is shelf space bought without ever touching the score field.

Fourth, and the record does not address this at all: nobody asks who composes the card. The only
upward path runs through `card_success`, and the card is composed by `wrap`, an agent act at the end
of a session, performed by the same agent in the same post-session state that "Where it came from"
names as the original hazard. If the agent that just fixed something also chooses which atoms go
into the card that will earn credit, the author's vote has not been removed. It has been moved one
hop downstream, into card composition. Whether that composing act is itself witnessed is recorded
nowhere we can find.

Fifth, on the downside: `fire_lower` decays toward the anchor and stops there, and the anchor is the
born value. A demonstrably harmful atom can therefore never rank below one that was never tried, so
"misleading" and "untried" are the same point in the ordering. That is the conflation this finding
exists to prevent, mirrored onto the downward path. The 1.0 floor in the earn-law constants is a
separate, lower bound approached by ordinary decay, not by `fire_lower`.

## Retractions and corrections

**Settled against the live engine (2026-09-10).** The 100.0 against 0.31 conflict is closed. The
running code declares an atom born neutral at a flat 100.0 on its internal scale, as printed in the
selftest above. The 0.31 in one node specification is a normalised readout of that same neutral
value on a nought-to-one scale. The two archive documents disagree because they quote different
scales, not different rules.

Kept as evidence of method: the fetch-as-score-delta finding of 2026-09-08 is a correction against
this finding's own mechanism, not against a rival design, and as of 2026-09-10 the mechanism it
condemns is still the one running.

Sources (release ledger ids): M-2397 M-3029 M-3192 M-3188 M-3028 M-3196 M-3109 M-2265
First seen: 2026-06-16
