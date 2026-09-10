# Round-2 zero-context skeptic verdict — THESIS.md

Reviewer: zero-context skeptic. Sources read: README.md, _gate/SKEPTIC-BRIEF.md, appendix/AP3-glossary.md,
findings/F10, THESIS.md, plus the cited findings F01/F02/F05/F06/F07/F08/F09 opened only to check
whether a THESIS sentence asserts more than the finding it cites.

**Verdict: FAIL — step 2 (evidence is assertion), one sentence.** Everything else passes; the failure
is a single overclaim against F06, and it is repairable by a phrase.

## Does a stranger understand the question?
Yes. "The question" is one paragraph and it is concrete: a model has a bounded context, a working
relationship does not end, how does the model keep remembering and remain the same collaborator. It
states what the work was *not* about (smarter or cheaper) before what it was, which is the right order
for a stranger. The failed first attempt — inject the identity at boot — is given immediately, with
the two-machine result and the harness cache, so the reader learns the shape of the problem from a
failure rather than from a definition. *harness* is glossed inline at first use.

## Does a stranger understand the chain?
Yes, and the chain is explicitly signposted rather than implied: "seven of them were forced by the one
before, and the other three sit off that line by design", with each of the three off-line ones named
and its role given (F08 a result, F09 a control arm, F10 a different axis). That sentence is the single
most useful thing in the document for a stranger, because it pre-empts the reader's question of why ten
findings are not ten steps.

The links hold when checked: store (F02/F03) → what a memory is for (F04) → how it ranks (F05/F06) →
the blind spot in pull retrieval (F07) → results off the line (F08/F09/F10). Each bold paragraph
carries its own limitation in the same paragraph rather than deferring it to the end — n=1 for F02,
"the curve stands, the causal reading does not" for F07, "two instances are not an ordering claim"
for F08. A stranger does not have to reach "What is not claimed" to learn that the evidence is thin
in specific places.

## Does a stranger understand what is not claimed?
Yes, and this is the document's strongest section. Five disclaimers, each falsifiable rather than
modest-sounding: not neural memory; no parameter changes; some measurements made by the process that
authored the material; the recall judge was found unwired once and could be again; and — the one that
matters most — no operator other than the author has reproduced the continuity result, named as the
open problem the release exists to address. A stranger closes the document knowing that the central
claim is unreplicated. That is the correct posture and it is stated without hedging language.

The economy section does the same job for a different temptation: it says the tier law, token economy
and reflexes "were not the point... they were the cost of the point", and then explicitly refuses the
adjacent claim — "That may be a result in its own right, but it is not one this report shows."

## Sentences that assert more than the finding they cite

Checked every quantified or causal assertion in THESIS against the cited file.

**1. FAIL — F06, demotion.**
> Passing over a memory demotes it; it can always be re-earned (F06).

F06 does not support the first clause. F06's retraction says the opposite of the mechanism this
sentence describes: *"the promise that an unused record fades toward neutral did not hold. Records only
moved when something acted on them. In practice demote-don't-delete ran on explicit negative signal, a
dispute or a losing impression, not on the passage of time"*. F06 further reports a reproduction in
which a score computed at two timestamps a year apart returned the identical value `112.5083001343761`,
and notes that the fix for this is *"still a recommendation, not a merge, at the time of writing."*

So passing over a memory demonstrably does *not* demote it in the shipped system. THESIS states as
mechanism the exact thing F06 retracts. This is the only place in the document where a sentence
asserts a behaviour its own finding measured as absent, and it is unmarked — every other thin claim
in THESIS carries its qualifier inline. Under the brief this is step 2: the evidence line behind the
clause is an intent quote ("demote don't delete") rather than the witnessed measurement, which went
the other way.

**2. NOTE, not a failure — F07, correlation.**
> Its confidence signal correlated with whether the surfaced memory was used, until a past-window
> control showed the signal tracks how busy the session is rather than how relevant the memory is;
> the curve stands, the causal reading does not.

Accurate to F07, including the retraction and the distinction between the surviving curve and the
struck causal reading. F07 adds one qualifier THESIS drops: *"Warm-versus-lukewarm separation persists
inside every window, so residual signal above busyness is plausible and unproven."* THESIS's "tracks
how busy the session is rather than how relevant the memory is" is slightly stronger than F07's
"substantially detects session-busyness" plus an unresolved residual. Directionally honest, marginally
over-tightened. Not worth a change on its own.

**3. Checked and clean:**
- "about 631 ingestion units", "175 KB conversation", "n=1", "lost on a wall-clock session limit" —
  all present in F02 with the same values and the same framing (F02: "a win on a wall-clock ceiling,
  not on fidelity"). THESIS also imports F02's own definition of "rebuilt" rather than assuming it.
- F08: "one day in September", "a ruling the owner had made in June", "two instances are not an
  ordering claim" — matches F08, which itself says "Two instances, four months apart" and routes
  recurrence to a hypothesis. THESIS says "On one occasion" twice in two sentences, which is
  redundant but errs safe.
- F09: "a narrow fact could be recalled on untrained phrasings", "a procedural skill was memorised
  rather than learned", "a stored fact stayed invisible mid-task" — three claims, three matches.
- F10: "That this is graded by model capability rather than universal is an expectation carried in
  F10, not a measurement" — this correctly imports F10's own demotion of that quotation. Good.
- F05: "born neutral", "browsing is free", "reading outside the door earns nothing, because the bank
  never saw it happen" — matches F05.
- F01: "could run for many turns pointing at those values without acting from them" — F01 says 11
  messages; "many turns" is vaguer than the finding, not stronger. Fine.
- "the 'weight' ECHELON tracks is a selection score in a database. It decides what gets read. It does
  not alter the network." — matches AP3 and F04. This is the report's most load-bearing negative claim
  and it is stated flatly rather than hedged.

## The one sentence to change
> Passing over a memory demotes it; it can always be re-earned (F06).

It asserts a decay-on-disuse mechanism that F06 measured as not happening and lists as an unmerged
recommendation. The rest of THESIS is calibrated; this sentence is not, and because it sits in the
same paragraph as the correct "never deleted", a stranger will read the whole demote-don't-delete
mechanism as shipped and working. Never rewritten here.
