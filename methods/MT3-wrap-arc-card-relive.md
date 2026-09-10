# A close-out ritual should consolidate its own index, not just append to it, and it should separate durable lessons from session state

**Claim.** A persistent-memory system that closes a working session with a single "wrap" step
will silently degrade unless that step does three things every time: writes durable lessons to
one store and operational state (goals, open items, journal) to a separate one, replaces its own
summary line instead of appending a new one on every run, and keeps a hard size ceiling on the
boot-time index so nothing silently truncates on load. Skip any of the three and the system either
pollutes its own recall signal with bookkeeping, or grows an index that quietly stops loading its
newest lines.

**Where it came from.** The mechanism is a memory substrate that an operator uses across many
sessions with a language model. Each session ends with a "wrap": distill what was learned, write
it as durable atoms, update a short human-readable index file that every new session reads first.
Two separate defects showed up during ordinary use, roughly two weeks apart, both traced back to
the same root cause: the wrap step only knew how to add, never how to consolidate.

**Evidence.** First, an escalation from the operator: "the wrap bleed are getting worse, need to
fix it and the skill asap." Measured live: each wrap added a resume line, a rollup, and pointer
lines, and consolidated nothing. The index file crossed its known boot-truncation ceiling (about
24.4KB) one day after an operator had manually reorganized it back under the limit. Separately,
recent wraps had appended lines below the marker that a separate automated sync process owns and
regenerates, where they could be silently eaten or duplicated. The fix, applied and measured the
same day, took the file from 25,044 bytes to 16,971 bytes while preserving all 133 internal links,
by replacing the resume line instead of chaining it and folding older entries into a rollup.

Second, a related but distinct finding, from a session spent trying to reconstruct which work
session produced which commit, after a project-lifecycle proof had flagged that a session ending
without a wrap can reach a "stopped, unwrapped" state from every point in the lifecycle with no
guard against it. The operator asked why that gap was being chased at all, and the measurement
against the bank answered it: atoms (the durable lesson writes) land on every single day the bank
was written to across a 65-day window; the wrap's own summary card lands on only 33 of those days.
An unwrapped session had not lost its knowledge. It had lost a summary and a resume menu. This
measurement covers one operator's usage over one 65-day window, not a general rate.

**Mechanism.** The system keeps two organs, not one: a bank of durable, weight-earning lesson
atoms, and a room of operational state — goals, open items, an append-only journal. The wrap verb
writes state to the room and only the distilled lesson to the bank, so bank recall is never
diluted by bookkeeping. Atom-writes happen continuously through the session (mid-session
`remember`/ingest calls), not only at wrap time, which is what makes an unwrapped session
low-stakes rather than a knowledge loss. The index file carries a mandatory size gate as part of
the wrap ritual: snapshot its internal links before editing, edit, and refuse to finish if the
result is over a fixed byte ceiling (roughly 18,000 bytes) or has lost a link. A write-zone law
fixes where new lines may land — never after the marker the automated sync process owns — so a
human wrap and a machine sync never collide on the same region. In five lines: (1) on wrap, write
distilled lessons to the bank, state to the room; (2) replace the single "latest" line in the
index rather than appending; (3) fold older entries into a dated rollup line; (4) snapshot links,
edit, diff, and refuse to finish over the byte ceiling; (5) never write below the machine-owned
marker.

**What it could still be wrong about.** The 65-versus-33-day measurement is a retrospective count
against one bank on one machine; it shows that lessons usually land before a wrap, not that they
always do, and a session that crashes very early (before any mid-session bank write) still loses
real work with no mitigation. The size-gate fix is also reactive: it was built after an escalation,
not before the first bleed, so the pattern this section describes is itself an instance of the
thing it argues for — a habit that lived in prose until it broke twice.

**Retractions / corrections.** The project-lifecycle proof (`STOPPED-UNWRAPPED reachable from
every node with zero guards`) was initially read as "knowledge destroyed." The follow-up
measurement corrected that framing directly: the loss is a summary and a resume menu, not the
underlying lessons, because those already bank mid-session through a separate, continuous
mechanism. A planned build to backfill session attribution retroactively, so this gap could be
detected across history, was cancelled at the design stage once the measurement showed the value
of doing so was low.

Sources: M-2014, M-2132, M-2131, M-3131, M-3367
First seen: 2026-08-16
