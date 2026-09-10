# A memory is a weight-adjustor, not a record

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

## Claim

What is witnessed here is a frame, adopted on 2026-06-05, and the four engineering decisions it
produced. The frame: treat a stored memory not as a text record you fetch and read but as an
adjustor, a compressed experience that, when a model chooses to read it, re-shapes how that model
behaves for the rest of the session. Under it, recall means applying adjustors rather than
retrieving text. Four decisions followed from it and are visible in the code today: one lesson per
file (an *atom*), because a dense multi-lesson file cannot re-shape cleanly; content-hash identity,
so replanting the same text is idempotent; a closed, typed, directed edge vocabulary describing how
one adjustor modulates another rather than librarian categories; and a free peek against a metered
fetch, so that only the act of choosing to apply a memory is recorded. That much is the finding.

The behavioural half of the frame, that reading a chosen memory re-shapes behaviour rather than
merely informing it, is stated here as a hypothesis and not as a result. Its falsifier is clean and
neither arm has been run: if the frame were wrong, splitting a fused file into single-lesson atoms
would change recall quality by nothing measurable, and storing model activations would work as well
as storing prose. The split arm was done as an engineering change with no before/after number taken;
the activation arm was never built at all, so its absence is evidence about what was prioritised and
not about what would have worked. Whether this recurs is stated as a hypothesis in appendix/AP2 and
hypotheses/.

## Where it came from

2026-06-05. The owner walked into a session that was designing ECHELON's memory the ordinary
way: store facts, define edges between them, traverse the edges, hand the resulting text back
to the model. He stopped it and corrected the foundation, in one sentence: *"we cannot use a
normal memories logic. because the memories are weight adjustor, transformer in a database."*
And then the scope of it: *"everything that touched weight, we will adapt."*

The correction came out of a specific injury. An earlier snapshot system had appeared to carry
identity across sessions, and then, on a change of hardware, "do you remember?" came back
empty. The apparent continuity had been the harness cache feeding conversation back in, not
anything the project owned. The lesson banked from that was blunt: if you do not own the
layer, you do not have it. When the June design started encoding state into the database, it
read as the same mistake in a new costume.

By 2026-06-23 the frame had hardened into the gate banner that gets prepended to every
project's memory index, so that any model on any provider can read the file cold and use the
substrate correctly. Claim one of four, in that banner: *"A memory is a WEIGHT-ADJUSTOR, not a
record. It stores the SEED that re-creates an understanding when you read it; recall RE-SHAPES
the model, it doesn't just inform it. So ONE lesson per file (an ATOM) — dense fused 'molecule'
files can't re-shape cleanly."*

## Evidence

The evidence is witnessed, not measured. There is no controlled experiment comparing
adjustor-shaped recall against record-shaped recall on a held-out task. What exists is a
recorded owner correction on a live design session, the design changes made in response, and
a later source audit of what the code actually does. Say that plainly: this claim is a frame
that produced engineering, not a measured result.

The correction survives verbatim in two independent places: a doctrine corpus assembled
2026-08-23 from session transcripts, and the atom banked at the time. That establishes provenance
and nothing more. Two copies of an instruction are one instruction, and the corpus's own metadata
label for it carries no evidentiary weight, by the 2026-09-08 rule recorded below.

The consequences are visible in the store. One lesson per file is enforced by the ingest path,
not by convention. Edges carry a directed, closed vocabulary of modulations (refines,
supersedes, instances, part_of, depends_on, contradicts, refs, subsumes) rather than free-form
categories. No activation encoding was ever built.

## Mechanism

Five lines of pseudocode, and the engine verbs that carry them.

```
write(lesson):    one lesson per file -> ingest    # a fused file is rejected as unclean
plant(atom):      id = hash(content); insert-or-ignore; born neutral
link(a, b, rel):  rel from a closed vocabulary of modulations, directed, idempotent
peek(intent):     recall --warm  -> spine previews, free, no credit earned
apply(atom):      remember       -> full body served through the earning door
```

`ingest` validates the markdown, resolves the canonical scope (the named partition of the bank the
lesson belongs to), refuses a scope mismatch without an explicit override, and skips a byte-identical body already banked elsewhere. Atom
identity is a content hash, so replanting the same text is idempotent while changed text
becomes a new row. `recall --warm` scores candidates against the current intent and returns
previews; it is free and earns nothing, which is what makes wide peeking affordable.
`remember` serves the full body through the door that records take-up, meaning whether an atom that
surfaced was actually pulled through and acted on rather than merely listed. An atom is *born
neutral*: it enters at a fixed score its author does not choose (F05). That split matters:
peeking at an adjustor is not applying it. Applying it is a choice, and only the choice is
recorded.

The seed rule follows from the same place. The store holds the compressed experience, not the
state it produces. You store the seed that re-creates the weight, and the weight re-forms at
read time in a model that chooses it. Same bytes read one way are rules you happen to know;
read another way they are yours. Because the difference lives in the reading, the adjustment
cannot be serialised.

## What it could still be wrong about

The word "weight" is doing dangerous work, and on 2026-09-08 a source audit of the engine
said so plainly. The audit found that the stored weight is a behavioural selection score
computed in a database, a number that changes which lessons surface and get reused. It is not
a modification of a language model's parameter tensors: *"The historical phrase 'weight-adjustor
/ transformer in a database' describes this behavioral aim; the inspected mechanism does not
modify an LLM's parameter tensors."* Anyone reading the phrase as fine-tuning is reading it
wrong. It describes an aim and an effect on behaviour, not an operation on a model's
parameters.

The deeper uncertainty is that the strong version is hard to test. "Re-shapes the model rather
than informing it" describes a difference in how a model reads its own history, and the
evidence for it is witnessed judgement plus design decisions that worked better afterwards.
The one-lesson-per-file rule has an independent justification (a shorter atom is a sharper
match for an intent query) that does not need the adjustor frame at all. The frame may be a
productive metaphor that produced correct engineering for reasons other than the ones it
gives. That would not make the engineering wrong. It would make the explanation wrong, and the
explanation is what this section is for.

The same audit found that the effective weight is not one consistent value across consumers. Name
this once, because it recurs across F05 and F06: there are two scoring surfaces. One is the *stored*
score, a column in the bank moved by the earn and decay constants. The other is a *recomputed*
score, derived at read time from a history of deltas, which is what warmth reads. Promotion
candidates read the stored one. The two can disagree, and neither the code nor the archive declares
one canonical, so an implementer rebuilding this must choose. If the number is the adjustor, the
adjustor has more than one value depending on who asks.

There is also a circularity in the take-up signal that the frame does not escape. Surfacing drives
reading, reading is what records take-up, and take-up drives surfacing. An atom that surfaced early
keeps surfacing; an atom that never surfaced stays neutral forever and is indistinguishable in the
store from one that surfaced and was rejected. So the store cannot separate "this lesson re-shaped
behaviour" from "this lesson was cheap to reach", and the reuse we point at as evidence that the
frame works is partly manufactured by the ranking the frame installed. The frame's central
distinction, chosen against supplied, is never varied either: every reader in the record is a model
reading a lesson inside a session that also holds the intent that retrieved it, which is exactly the
configuration in which ordinary in-context relevance would produce the same behaviour change.

## Retractions / corrections

- **2026-09-08, correction, kept in place.** The phrase "weight-adjustor / transformer in a
  database" is a description of behavioural aim. The inspected mechanism does not touch model
  parameters. The two must not be conflated.
- **2026-09-08, correction.** A metadata field on an atom that labels its evidentiary basis
  (execution, owner, inference) is display only. It does not establish proof, change ranking,
  or earn weight. An atom does not become heavier by asserting that it was witnessed.
- **2026-09-08, gap, open.** The owner ruled that banking a new atom should return the atoms
  linked on its edges at write time, because that is the cheap window in which a stale or
  lying neighbour can be disputed. The write path resolves references and creates edges but
  never surfaces the neighbours back for review, so a contradicting neighbour is noticed only
  when a later agent steps on the trap it causes. No shipped fix was found. It remains open.

Sources (release ledger ids): M-2207, M-3189, M-3190, M-2260, M-2261
First seen: 2026-06-05
