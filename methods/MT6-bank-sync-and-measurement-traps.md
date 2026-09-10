# A memory bank syncs safely by replaying scoring events, not merging final scores, and its bugs surface only by measuring the live database

**Claim.** Because a memory atom's usable weight is recomputed at read time from its full history
of earning events rather than stored as a running total, two copies of a memory bank (a laptop copy
and a cloud copy, say) can sync by replaying the individual history events each side is missing,
tagged by which bank witnessed them — never by merging the two sides' final scores directly. Most
of the concrete bugs and costs in that sync design were found only by measuring a live, growing
database, not by reasoning on paper, and each measurement carried its own trap.

**Where it came from.** Each memory is a row with a running score plus a history of earning events
(timestamp, amount, and now which bank witnessed it). The score shown to the reader is not the
stored number; it is recomputed on every read from the history with time-decay applied per event.
Building two-way sync between a local bank and a cloud-hosted bank — so a memory written on either
side reaches the other, and the sync channel doubles as a backup — surfaced a design fork:
replicate the final numbers, or the events that produced them. An independent reviewer, working
from the live schema and code, failed the first design and forced the second.

**Evidence.** The design document states why the event-level approach was required: "the merge
unit is the history event" because the score "recomputes from full history." During the build, two
banks that earned weight on the same memory in the same second produced entries that looked
identical under the original merge rule, so the count-based logic silently swallowed one —
"the local 3 fetches ate the peer's 2 in the first test run." The fix tagged every event with its
origin bank, so identical events from different banks are both kept, and only a genuine re-send is
dropped. With that fix, a full round trip between two real banks passed 22 of 22 checks: both
converged to the same memories and history, and a second cycle with nothing new produced zero
operations, no drift.

A second, unrelated measurement showed how expensive naive change-logging gets: one live database's
sync journal, which logs every change for replication, had grown to 314 of 465 megabytes — 68
percent of the file — and of its roughly 102,000 logged rows, about 93,700 were routine
weight-decay ticks, each re-logging the memory's full content. Splitting the trigger so a
weight-only tick logs a small payload (345 bytes) instead of the full row (3,302 bytes average) cut
per-tick log size roughly tenfold. That same pass is the clearest example of the title's trap: an
audit found the 465MB/314MB/102,410 figures did not match the database when the fix shipped, which
by then held about 2,400 rows and 8 megabytes — stale, or from a different copy — and the audit's
own conclusion was "re-measure before quoting it again," even though the fix's direction held.

Two further traps, same shape. A keyword search across a memory bank's roughly 2,100 entries
estimated about 120 belonged to one sub-project; reading each entry individually found all but one
were core doctrine — the sweep's estimate was, in the record's own words, "a mirage." And because
the database keeps recent writes in a side file, a plain whole-file copy taken while open can
silently produce a stub with no tables instead of raising an error — it hit the routine backup and
the pre-restore safety copy alike, so the copy meant to undo a bad restore could itself be empty.

**Mechanism.** In five parts, buildable independent of this specific system:

1. Never store weight as a number to merge; store an append-only list of dated, amount-tagged,
   origin-tagged events, recomputing the score from that list at read time — merging becomes
   commutative, since applying the same events in any order gives the same result.
2. When two copies exchange history, drop an event as a duplicate only if it matches on
   timestamp, amount, and origin together; keep both if the origin differs, even on a match.
3. Split change-logging into a narrow path for routine, high-frequency mutations carrying only
   changed fields, and a full-payload path for structural changes, guarded by conditions proven
   (not assumed) mutually exclusive and jointly exhaustive.
4. Use the database engine's online-backup interface for a live write-ahead-logged database, never
   a plain file copy; verify a backup by reading a known table, not by checking the file exists.
5. Before quoting a measured system-size number a second time, re-run the measurement against
   current state — "stale measurement" is a named failure mode.

**What it could still be wrong about.** The round trip is strong within the scenario tested — two
banks, one sync-cycle pattern — but is not proof the merge law holds under every interleaving of
concurrent writers; the tie-breaking rule is a heuristic if two independent events collide on all
three fields by chance. The journal fix's real-world savings figure is unverified against the
current database; only the per-row ratio, roughly tenfold, is defended by fresh measurement.

**Retractions / corrections.** The journal-diet audit retracted its headline "68% of the bank,
102,410 rows" figure as unreproducible at ship time, keeping the underlying fix. The "~120 atoms
belong to the sub-project" estimate was retracted after a one-by-one read found one genuine match.

Sources: M-2293, M-2301, M-2755, M-2605, M-2212, M-2243, M-2296, M-2962
First seen: 2026-08-02
