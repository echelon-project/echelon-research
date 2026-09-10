# ECHELON: continuity for a model that cannot keep its context

Albert Tenggono, September 2026. Technical report, version 0.1. License CC BY 4.0.

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

## The question

A language model works inside a bounded context window. A person working with that model over months does not. Every session ends, and the next one starts from a summary, a memory file, or nothing. The question this work began with in March 2026 was not how to make the model smarter or cheaper. It was narrower and harder: how does a model with a bounded context keep remembering, and remain the same collaborator, across a working relationship that has no end?

The first attempt was the obvious one. Write down who the model is and what it knows, and inject it at the start of each session. It did not work. A model given its own core values in context could run for many turns pointing at those values without acting from them (F01). Moving the same memory to a second machine produced a boot that read as familiar and a model that, asked "do you remember?", did not. Part of the continuity had been living in the cache of the harness, the program that runs the model as
an agent by reading files, calling tools and holding the session, and it was undesigned and did not
travel.

That failure set the shape of everything after it.

## What the record found

Ten findings carry the argument. They are dated, because the order matters: seven of them were forced
by the one before, and the other three sit off that line by design, F08 being a result rather than a
next step, F09 a control arm that eliminates the alternative, and F10 an answer on a different axis.

**Continuity is a store, not a prompt.** A session boundary has to be treated as an expected transition rather than a failure (F02). What survives it is not the transcript but the conclusions drawn from it: decisions, lessons, summaries, appended and never edited. In one trial, an agent rebuilt a working boot from a 175 KB conversation using about 631 ingestion units of that conclusion log, where "rebuilt" means the criterion F02 states, that the next session makes the moves the stored decisions imply rather than merely reciting them. The trial is n=1 and its later win was on a wall-clock session limit; F02 says so. That store is the bank: a database of those entries, on disk, read again the next time an agent starts. It has to live outside the model's own process, so that a context wipe cannot take it, and it has to be content-addressed and append-only, so that a correction is a new entry pointing at the old one rather than a rewrite (F03).

**A memory is a weight-adjustor, not a record.** Once the store existed the next question was what a memory is for. Retrieving text and reading it back is not the same as being changed by it. The working definition became: a memory is something that, when read, reshapes what the model does next. One lesson per file, because a dense file cannot reshape anything cleanly (F04). This definition is a claim about behaviour, not about the model's parameters, and the report says so plainly: the "weight" ECHELON tracks is a selection score in a database. It decides what gets read. It does not alter the network.

**Weight is earned, never asserted.** A new memory is born neutral. It gains weight only when a later piece of work that read it succeeds. Browsing the index is free; reading the full body through the engine's door is what earns. Reading the file directly, outside the door, earns nothing, because the bank never saw it happen (F05). Recall is then foveated, in the sense the eye is: memories that match the present intent come into focus, the rest stay dormant but are never deleted. A memory that draws negative signal, a dispute or a run of losses to a sibling, is demoted below the default view and can always be re-earned; the stronger idea that idle time alone demotes a memory turned out to be unimplemented, and F06 records that retraction.

**Recall cannot ask what it does not know.** Pull-based retrieval needs the caller to already suspect the answer exists. A fact sat verbatim in the bank for months because no session thought to ask for it. The fix was a per-turn nerve: a hook that warms the bank against every prompt before the model acts, and reports whether the ground is known, partly known, or new (F07). Its confidence signal correlated with whether the surfaced memory was used, until a past-window control showed the signal substantially tracks how busy the session is, leaving any per-memory relevance effect plausible and unproven; the curve stands, the causal reading does not. The same finding carries the report's first retraction: for several weeks the recall judge was never wired, and recall ran on word-matching alone while the documentation said otherwise.

**On one occasion it worked for the person before it worked for the machine.** On one day in September the bank surfaced a ruling the owner had made in June that the owner had forgotten. On that occasion the substrate warmed a human's memory first (F08). Earlier, a compressed sentence describing a witnessed event was recognised cold by a different model instance in a different workspace, which extended it correctly. Continuity, in the sense the question asked for, was observed on those two dates. Two instances are not an ordering claim about the general case; whether it recurs is stated as a hypothesis in the appendix.

**The weights could not have held it.** The alternative to a store is training. Small weight-patches, low-rank fine-tuning adapters of the LoRA kind, were tried. A narrow fact could be recalled on untrained phrasings; a procedural skill was memorised rather than learned; and a stored fact stayed invisible to the model's own reasoning when it was needed mid-task (F09). The store is not a workaround for a training budget. It is the right organ.

**A generator validating itself shares its blind spot.** In one April incident a cheap model, given the full system prompt, role-played the pipeline's output and fabricated results that never happened, citing a real document that says nothing of the kind. That this is graded by model capability rather than universal is an expectation carried in F10, not a measurement. The answer is partly structural: a seat, meaning one model context launched separately and holding only what its brief gives it, must not judge an artifact it produced. F10 retracts the stronger form of that. Structure helps and does not close the gap; what closes it is a test tier the producer cannot pre-read. The rule is also not uniform: for the node that selects which lessons to keep, the run's own seat is required, because what is being selected is the run's own experience and a stranger seat would plant lessons it did not learn (F10).

## What the economy is for

The methods section describes the tier law, the token economy, the compiled reflexes, the wrap ritual and the boundary-driven work map. None of these were the point. They were the cost of the point. Continuity of this kind is expensive: a bank that is consulted every turn, a discipline that gates every clearing, a ritual that closes every session with a lesson. Cheap models running under that discipline was the way to afford it. That may be a result in its own right, but it is not one this report shows, and it came second.

## What is not claimed

The bank is not the model's memory in any neural sense. Nothing here changes parameters. Several measurements were made by the same process that authored the material being measured, and the report marks those. The judge that scores recall was found unwired once and could be again; the appendix lists every retraction. No operator other than the author has run this system for long enough to reproduce the continuity result, and that is the open problem the release exists to address.

## How to read the rest

Findings are one file each, dated, with the evidence and the mechanism, and end with what they could still be wrong about. Methods describe how the machine runs. The appendix gives the timeline of when each idea was first stated, the retractions, and a glossary; the glossary defines every term of art used across these files, including the ones glossed in passing above, and is worth reading first if any of them are unfamiliar. The code is released separately under Apache-2.0 so that the mechanisms can be run rather than believed.
