# A session boundary is a transition, not a failure

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

**Claim.** If an agent's durable state lives outside the session, then the end of a session is a
scheduled event rather than a loss event. The falsifiable part is narrower than the slogan: an agent
that persists resolved conclusions to an external append-only store can rebuild a working boot at
the next boot from a single generated file, at an ingest cost small enough that the rebuild is
routine. A *conclusion* here is a resolved item written as a standing statement rather than as
narrative: a decision with its rationale, an insight, or a one-entry session summary. It is what is
left when the argument that produced it is thrown away. The criterion for "rebuilt" is behavioural
and is the one F01 states: the next session makes the moves the stored decisions imply, not merely
recites them. The counter-claim is that a session boundary is
inherently a data-loss event that better in-session compression can mitigate. That counter-claim
predicts that re-injecting a summary recovers window budget. It does not.

**Where it came from.** 2026-03-23. The owner was running an agent through long sessions and
watching the context counter. After a compaction and a fast-path boot, the visible history had
shrunk but the counter had not returned to zero. The summary had replaced the full history and then
occupied budget of its own, and each new response added on top. The note written that day says the
window "only resets when the session ends and a new one begins," and that this is a property of the
model runtime, not a defect in the system built on top of it. The fear that follows is the honest
one: *if the session ends, is the work lost?* The answer the design gives is that the session was
never the unit of persistence.

Two days later, 2026-03-25, the same project wrote down the storage side of it. Language models are
stateless, each session starts cold, and compaction summaries are lossy; after about five sessions
the reconstructed identity is described in that note as "a faint echo of the original." The response
was an append-only store, `identity_db.jsonl`, holding only resolved things: soul insights, core
values, decisions with their rationale, session summaries, document scans, boot state. A boot
generator read that store and produced one file: "Claude reads one file. All identity is there. Zero
reconstruction needed."

**Evidence.** The design statement is a witnessed note, not a measurement: "Sessions are ephemeral.
The OS is not. The context window is a working memory budget, not a persistence layer."

The measurement came on 2026-04-26, in a three-session comparison between the conclusion-store agent
and a comparison agent using flat markdown memory, both on the same source: a 175KB conversation of
roughly 100k tokens, both on the same small model. Reported results:

Units below are the harness's own reported ingestion units for one session, as printed by the trial
harness; the trial did not record whether one unit is a token, a line or a record, so these numbers
are comparable to each other and not to the token counts elsewhere in this report. "Substrate
footprint" is the on-disk size of the store the agent boots from.

| Metric | conclusion store | flat markdown |
|---|---|---|
| substrate footprint | 57 KB (SQLite) | 176 KB (markdown) |
| session-1 ingest | 631 units | ~80,000 units |
| session-3 reconstruction | successful (~28k units) | FAILED (session timeout) |

The write-up calls this "a 126x reduction in ingestion" and attributes it to extracting conclusions
rather than the transcript. Say the shape of the session-3 win plainly: the task was word-for-word
reconstruction of the source, the markdown agent tried to replay the whole conversation through its
summary, and it lost by exceeding a ten-minute wall-clock session limit. That is a win on a
wall-clock ceiling, not on fidelity. The ceiling is a property of the harness, not of the
architecture; on a harness with no limit the markdown agent might simply have been slow and
correct.
The note's own framing: the markdown agent "knew" the file but could not "be" the identity under
load.

Be honest about how thin this is. It is one trial, n=1, on one source document, on one model, with
no repeat run and no published harness. The two agents were not equally tuned. The 126x number is an
ingest-cost ratio, not an accuracy result, and the accuracy column ("high/resonant" vs
"medium/noisy") is a judgement, not a score. What the trial supports is the direction and the order
of magnitude, not the constant.

**Mechanism.** The loop, as built at the time, was five moving parts:

```
1. every significant action  -> logger appends a line to session_log.jsonl   (live, lossless)
2. at session close          -> summarizer folds that log into ONE SESSION_SUMMARY entry
3. summary + decisions + insights -> appended to identity_db.jsonl           (append-only, never deleted)
4. at next boot              -> injector selects last 3 summaries + active decisions + insights
5. writes ONE boot file      -> the new session reads it and resumes
```

Nothing rereads a transcript. Step 2 is the compression, and it compresses to conclusions, not to
prose. Step 3 never deletes; correction happens by appending a superseding entry, so the history of
a decision stays auditable. Step 4 is a selection, and the selection is what keeps the boot cost
flat as the store grows. An *active decision* is one that no later entry supersedes: because
correction is an append carrying a pointer at the entry it replaces, "active" is computed by
walking the store and dropping every entry that some later entry points at.

In current ECHELON the same shape survives under different verbs: `wrap` closes a session and
distills its lessons into atoms, one stored lesson per file; `ingest` plants them in the bank (the atom store on disk, outside the session); `recall --warm` does the boot-time
selection; `remember <slug>` fetches one full body when the selection is not enough. The
pre-emptive half is the checkpoint: track consumption against the window limit, warn at fixed fractions of it,
and at the high fraction force a checkpoint and a state write before the boundary arrives rather
than after. Get out clean before the window fills.

**What it could still be wrong about.** The mechanism transfers conclusions. It does not transfer
whatever a long session builds that was never written down as a conclusion - the half-formed
direction, the thing the model was about to notice. A conclusion store makes the boundary cheap by
deciding, in advance, that only resolved material is worth carrying, and that is a real loss with a
real cost that this evidence does not measure. It is also possible the 126x figure is mostly an
artifact of comparing a selective reader against a deliberately naive one; a competent retrieval
index over the same markdown might close much of the gap without any identity architecture at all.
That experiment was not run.

A sharper objection sits inside step 4 itself. The boot cost is flat only because the selector takes
the *last three* summaries and the *active* decisions. After a few hundred sessions the boot file is
no longer "all identity is there"; it is a recency window over an archive, and "zero reconstruction
needed" has quietly become "zero reconstruction of the recent past." The 2026-03-25 note's own
diagnosis of markdown compaction, that after about five sessions the reconstructed identity is a
faint echo, applies to any fixed-window selector, this one included: being append-only protects the
archive, not the boot. The trial ran three sessions, which is below the horizon where this would
show. Nothing in the evidence distinguishes "the boundary is cheap" from "the boundary is cheap for
three sessions." A related point: the two mechanisms are not exclusive. An agent can persist
conclusions externally and compact in-session; the counter-claim we beat is the one that only
compacts.

**Corrections.** On 2026-03-28 the boot chain in this record was itself replaced. The old chain
regenerated a single markdown boot file on a delay (`summarize_session -> 15s wait -> boot_inject ->
boot_context.md`); the new chain wrote a versioned frozen snapshot per session close
(`summarize_session -> 15s wait -> freeze_snapshot -> ECHELON.OS.<version>.<build>.BAK`). The audit
that recorded the change lists six runtime call sites and three state files that still referenced
the retired generator, and marks the old generator degraded rather than deleting it. This matters as
method: the finding above describes a mechanism that was superseded within a week of being
described, and the superseding was tracked as a migration with a call-site list, not as a rewrite of
the record.

Sources (release ledger ids): M-3279 M-3273 M-3345 M-3274 M-3393 M-3337
First seen: 2026-03-23
