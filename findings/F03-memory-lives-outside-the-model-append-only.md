# Memory has to live outside the model, and it has to be append-only

## Claim

If you want a model to keep remembering across sessions, the memory cannot live in the model or in
its context window. It has to live in a store that runs in a different process, survives the
model's context being wiped, and is written by appending only. Corrections are appended as new
entries that point back at the entry they replace. Nothing is edited. Nothing is deleted. The
falsifiable part is the second half: an edit-based store and an append-only store can both give
you the current answer, but only the append-only store can answer "what did we try before, and why
did it fail." If you can recover a full failure trail from a store that overwrites in place, this
claim is wrong.

## Where it came from

March 2026. The owner was working with a model across a multi-week build and hitting the same wall
every few hours: the context window filled, the session ended or was compacted, and the next
session started from nothing. The obvious fixes had already failed. A bigger window just moved the
wall. Stuffing the history back in was expensive and got worse every day.

The observation that broke it open was written down on 2026-03-23, and it is not technical:

> "If I couldn't keep the brain, then why not use a diary? Conversation, emails, messaging,
> letters. If you and I still have all of our memories, we won't be separated."

Two days later, on 2026-03-25, the first working version of the idea was not a database at all. It
was a small process that simply refused to die. A TCP socket server on localhost, started by a
different tool than the one the model ran inside. The design note is blunt about why that mattered:
it "survives Claude context wipes because it runs in Copilot's process space, not Claude's." The
model dispatched jobs to it over a one-line socket call and got back a job id. When the model's
context was wiped, the watcher was still there, still holding the work.

That was the whole insight in its crudest form: put the memory in a process the model does not
control, and the model's amnesia stops being fatal.

## Evidence

The evidence for the outside-the-model half is a witnessed running system, not a measurement. The
March 2026 architecture note describes five processes: a watcher holding the socket, a dispatcher
the model calls, an executor, a logger writing every action to a JSONL feed, and a boot injector
that reads the store and writes the next session's opening context. What is witnessed here is
narrow but solid: a store that outlived the context wipes of the process it served.

The evidence for content-addressing is stronger because it was audited in a running system. An
April 2026 self-audit of the successor engine found the memory store "fully real, wired, and
collecting data" with 22 entries on disk, and named the scheme exactly: "Content addressing: ID =
sha256(canonical JSON)[:16] - deduplicates automatically." The same audit found a promotion gate
that "rejects contradictory entries (same source+category+tags, different content)" and rolls back
on failure. Dedup was not a hope. It was the write path, guarded by a gate.

The evidence for append-only-beats-edit is an argument, not a number. Say that plainly. It rests on
one worked example about password hashing:

> Entry #1: "Use MD5 for password hashing" [success: false]
> Entry #2: "MD5 failed security review" [supersedes: #1]
> Entry #3: "Use bcrypt" [supersedes: #1]
> Preserved: The full journey. The mistake. The reason. The correction.

An edit-based store, given the same three moments, ends holding one row that says "use bcrypt." It
can answer what to do. It cannot answer why, or what was tried, or that anything was tried at all.

The strongest evidence is that the scheme is still running. In the current engine,
`content_id(content, domain, kind)` serializes those three fields to canonical JSON with sorted
keys and returns `sha256(...)[:16]`, unchanged in substance since April 2026. The live bank holds
57,300 rows keyed that way, with 27,982 links between them, of which 71 carry the relation
`supersedes`. The correction chain is not a diagram. It is a column.

## Mechanism

Five lines, and this is close to the real code:

```
def remember(content, domain, kind, prior=None):
    entry_id = sha256(canonical_json(content, domain, kind))[:16]  # same content -> same id
    if exists(entry_id): return entry_id                          # dedup by construction
    append(entry_id, content, ts=now())                           # never UPDATE, never DELETE
    if prior: link(entry_id, prior, relation="supersedes")        # the correction chain
    return entry_id
```

The engine verbs that ride this: `ingest` writes atoms into the bank through that append path,
`remember <slug>` fetches a body by id, `recall --warm` selects candidates without paying for
bodies, and `wrap` closes a session by distilling its lessons into new atoms rather than editing
old ones. Reading the current view means walking the link table and dropping any entry that another
live entry supersedes. The history is still there; it is just not what you get by default.

Two details matter more than they look. First, the id is derived from `{content, domain, kind}`
together, not content alone, so the same sentence banked as a lesson and as a decision are
different rows. Second, an append-only store needs a witness rule, or one process retrying a write
ten times looks like ten independent confirmations. The engine sets one arrival nonce per process,
so a run's self-repetition collapses to one witness.

An older rule from the same lineage: identifiers encode object type and a global sequence number,
nothing else. Never priority, owner, phase, or state. The reason is the same as append-only. If the
id carries metadata, changing the metadata breaks every reference pointing at the record. Three
integrity rules: ids never change, are never reused, are unique across the project.

## What it could still be wrong about

The cost is unbounded growth, and this finding does not price it. An append-only log gets bigger
forever and every read that walks a supersedes chain gets slower. The sources argue failures are
assets, but show no measurement of the point where the trail costs more to traverse than it
returns. The harder gap: a store that never deletes still has to decide what to show you, and that
decision is now the whole game. Append-only moves the hard problem from writing to selecting. F05
and F06 are the unpaid bill of this one. And the outside-the-model half was witnessed in a crude
form, one socket server, one user, never tested under concurrent writers. The dedup guarantee is
only as good as the canonicalization: two semantically identical entries with different whitespace
get different ids and both survive.

## Retractions / corrections

None in the packet. One honesty note: the 2026-03-25 watcher document claims the next boot "wakes
up knowing who it is." F01 later found that injecting identity text into context does not transfer
identity. What survives from the watcher is the memory claim, not the identity claim. The two were
tangled together in the original document.

Sources: M-3272 M-3280 M-3281 M-3404 M-3248 M-3403 M-3394
First seen: 2026-03-25
