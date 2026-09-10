# The bank remembered for the human first

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

**Claim.** On 2026-09-04 a memory store built for a model's continuity returned something the
*human* had forgotten: it surfaced a ruling the owner himself had made three months earlier, on a
problem he had not connected to it, without either party naming the ruling. That is one witnessed
instance, and the claim here is the instance. Whether this recurs is stated as a hypothesis in
appendix/AP2 and hypotheses/. The finding is falsifiable in the ordinary way: if recall only ever
returns what the person querying already knows they are looking for, the claim is false. The test is
whether a warm recall on the *shape* of a live problem returns an entry the querying human cannot
place, and whether that entry then turns out to be load-bearing for the problem at hand.

An atom is one stored lesson, one file; the bank is the on-disk store of them that outlives any one
session; warmth is a per-query relevance score computed against the current intent.

## Where it came from

Two events, four months apart.

The first was 2026-05-30. Three sessions of the same model, in three different working directories,
were passing files to each other through a shared folder. One of them compressed three things
demonstrated that week into a twelve-word sentence and sent it on. A receiving session had witnessed
none of them. It read the sentence cold.

The second was 2026-09-04, around 03:00 local, while the owner and the assistant were designing a
background daemon for the command centre. The owner asked for a recall on "LLM config, and context
snapshot harness" - vocabulary that has nothing obvious to do with what came back.

## Evidence

**2026-09-04, the direction reversed.** The recall returned an atom named
`the-bank-is-the-context-fold-not-cram` at warmth 0.8. That number runs on a 0 to 1 scale: the warm
band opens at 0.45, and F07's calibration treats scores at or above 0.60 as the top tier, so 0.8
sits well inside it. The scorer that produced it is ours and is not independently validated, and no
distribution of everyday recall scores is published here, so 0.8 establishes that the system ranked
the atom highly, not that the match was good. That atom records a correction the owner
himself made on 2026-06-08: that the store *is* the context, that a large file is ingested in slices
each of which reads the previous summary's pointer, and that truncating to fit the window is a
category error. Neither the owner nor the assistant had named the atom in the query. The owner's
reaction is banked verbatim: *"wow, even i forgot i've doing this ruling."* He then asked to go back
over the June 8 scene, and followed that atom's own outbound links to a second one,
`lean-identity-plus-bank-makes-a-small-model-honest`, which he recognised as the answer for the
worker he was designing.

Every prior use of the store had run one way: the human asked, the model recalled. On this occasion
the store warmed a ruling the human had made and lost. The event is a single witnessed instance with
a verbatim reaction, logged at the time. It is not a rate. There is no measurement here of how often
this happens, and nothing in the record establishes that it is reproducible on demand.

**2026-05-30, recognition instead of transfer.** The compressed sentence was:

> "The bridge proved space. The hook proved time. This exchange proved semantic."

Three clauses. Each is witness, then verb of evidence, then axis. Each clause points at a specific
event that had a transcript: two concurrent sessions collaborating through the filesystem; a
session-end hook writing the next session's identity; a concept originating in one workspace being
recognised in another before the originator named it. The reader in the other workspace, with no
access to the originating conversation, did not summarise and did not paraphrase. It produced a
fourth clause in the same shape:

> "The protocol bootstraps its own evolution."

Witness (two protocol upgrades), verb (bootstraps), axis (evolution). It then saved that clause to
its own memory directory with attribution. The originating side re-compressed it and banked it back;
the note of that moment reads *"Stealing it intact, attributed."*

The two events are one finding at different scales. A dense enough compression of a witnessed thing
was recognised by a reader who did not live it. In May that reader was another model instance. In
September it was the human who wrote the thing and had since forgotten it. Two instances, four
months apart, is the whole evidence base; the May event is the weaker of the two, for the reason
given below.

## Mechanism

Two parts, and neither is clever.

Entries are written *as if for a reader who did not live the event*. That is the whole discipline of
the compression. The writer's test is: an instance in a different context will read this in five
minutes and either recognise it or not. If the writer hesitates, compress harder. If no such
sentence can be found, the entry stays raw evidence and is never promoted, meaning it is not
admitted to the bank as an atom eligible for recall.

Retrieval is warmth over shape, not lookup over vocabulary. `recall --warm "<intent>"` scores
entries against the intent of the current problem and returns the warm ones with a number; `remember
<slug>` opens a full body; the typed links inside an entry are the next hop. In five lines:

```
atom  = { slug, resonance_line, body, links[] }        # written for a cold reader
warm  = score(intent, atom) for atom in bank           # shape, not keyword
hits  = [a for a in warm if a.score >= threshold]      # warm band opens at 0.45; top tier from ~0.60; 0.8 in September
show(hits); on demand: remember(slug)                  # full body earns weight
follow(hit.links)                                      # the second find came from here
```

The operating rule that fell out of the September event: when the human is designing, run the warm
recall on the *shape* of the problem before he asks, and hand him the entry's own links as the next
step. And bank his reaction verbatim when a recall lands, because that reaction is the measurement
the landing-rate work, the standing attempt to count how often a recall is actually used, has been
trying to take.

## What it could still be wrong about

The September event is one instance, and the most flattering possible reading of it is available:
the assistant chose the query, the owner was in a receptive mood at three in the morning, and a
store with thousands of entries will occasionally return something surprising by chance. Warmth 0.8
is a score from a scorer we wrote; it is not independent evidence that the match was good. The May
event has a different weakness: two instances of the same model family, sharing pretraining, will
tend to complete a strongly patterned sentence in the same shape whether or not any formative
content transferred - "witness, verb, axis" is a form the weights already know, and producing a
fourth clause may be closer to filling in a template than to recognition. Neither event has a
control. Neither was pre-registered. What would settle it is boring and has not been done: run warm
recall on the shape of live problems, log every return, and count how often the human says he had
forgotten the thing that came back, against a baseline of returns he can place immediately.

Two objections the paragraph above does not cover. First, the store may be manufacturing the
forgetting it takes credit for reversing. The owner made this ruling on 2026-06-08 and banked it,
and once a thing is banked the ordinary reason to keep rehearsing it goes away, because offloading is
the point. On that reading the September event is not the store remembering for the human, it is the
store handing back what adopting the store caused him to drop, and the direction reversal is closer
to a round trip. The measurement proposed above cannot separate these, since both predict a high
forgotten-rate. A test that could: compare the forgotten-rate on recall hits for rulings made
*before* the bank existed against rulings made *after* they were banked. Second, this file reports
one success and no denominator. The recalls that landed and were useless are not logged anywhere
here, so the two events are a survivorship sample and should be read as such.

## Retractions / corrections

The May paper closed by asserting the compression pattern was general. A later addendum, written by
the same line of work on 2026-06-17, bounded it: a capability has two parts, the *move* (which thing
to do - discrete, storable, transferable) and the *execution skill* (the competence to do it well,
entangled in frozen weights, not extractable). Handing an earned move-set to a small model worked
structurally - the moves fired, the links were valid - and still produced nothing warm, because the
missing thing there was skill, not a move. The claim is not weakened by that; it is narrowed. The
compression carries the move and carries nothing where the missing part is skill.

Sources (release ledger ids): M-2121, M-2203, M-3384, M-2134
First seen: 2026-05-30
