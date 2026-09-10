# AP3 — Glossary

Defined from the sources in this report (`findings/`, `methods/`, `_ledger/claims.jsonl`). One or
two sentences each, no jargon inside the definition itself.

**atom** — A single stored lesson: one claim, one piece of evidence, one file. Atoms are the unit
the memory substrate reads, writes, and scores; nothing smaller is stored on its own.

**card** — A record of one attempt to do a piece of work, including which atoms it drew on and
whether it succeeded. A card is what lets the substrate later credit or discredit the atoms it
used, because the outcome is attached to the attempt, not floating free. In older documents "card" also names an ordered sequence of atoms that composes a procedure; both senses share the credit path (a card that succeeds credits the atoms it loaded), and F05 uses the older sense.

**arc-card** — A card written at the end of a work session that closes out that session's arc: what
was attempted, what changed, and a pointer back to the previous arc-card, so the sequence of
sessions forms one continuous line even though each session's own context is thrown away.

**bank** — The place memory lives outside the model: a single database file of atoms, on disk,
partitioned into scopes, that survives a context wipe and is read again the next time an agent
starts working. The bank is the durable side of the boundary; the session is the disposable side.

**scope** — A named partition of the bank (for example, one project's slice of it). Writing or
reading with the wrong scope either pollutes another project's memory or fails to find memory that
is actually there.

**warmth** — A per-query score describing how relevant a stored atom is judged to be to the current
intent, used to decide what to bring into context. Warmth is a computed number, not a fixed
property of the atom.

**warm / lukewarm / cold** — Three bands a recall result can fall into: warm means the atom matches
closely enough to load automatically, lukewarm means a bounded manual check is worth doing, and
cold means the atom is left out of the current context entirely, though it still exists and can be
found later.

**recall** — The verb that reads matching atoms into the current context without changing their
score. It corresponds to seeing a search result: looking is free, it does not by itself count as
using the result.

**remember** — The verb that reads the full body of one specific atom and, unlike recall, counts as
using it — the act that can raise that atom's weight if the work it informs later succeeds.

**peek vs fetch** — Peek is looking at a short preview of an atom (free, does not earn or spend
anything); fetch is retrieving the atom's full content for use (paid, in the sense that it is the
act that can later be credited if the work built from it pays off). The distinction exists so that
scanning does not get scored the same as using.

**take-up** — Whether an atom that surfaced was actually pulled through the fetch door and used in
the work that followed, as opposed to merely appearing in a recall result. Take-up is the only
signal the store records about use, which is why it is load-bearing and why it is circular: what
surfaces is what gets taken up, and what gets taken up is what surfaces.

**weight** — A per-atom number that determines how likely that atom is to surface in future recall.
Weight is a selection score kept in a database. It is not a parameter inside the language model
itself, and it never changes what the model can do outside of this scoring step. See *effective
score (two surfaces)* for the fact that "the weight" is not one number.

**decay** — The gradual reduction of an atom's weight over time when it is not being used,
computed at the moment it is read rather than stored as a pre-aged value. Decay is meant to let
old, unused evidence fade toward a neutral baseline, at a rate set by how perishable that atom's
type is.

**demote** — What happens to an atom whose weight falls below the threshold for automatic recall:
it stops appearing by default, but it is not deleted and can rise back into view if it earns weight
again through later use.

**supersedes** — A pointer from a newer atom to an older one it replaces. Corrections are written
as new atoms carrying a `supersedes` link rather than by editing the old atom in place, so the
history of what was believed and when stays intact.

**reflex** — A compiled guard that pattern-matches a tool call and fires automatically, before the
call executes, without the model spending a reasoning turn to recall and reapply the underlying
rule. Reflexes exist so that a rule that would otherwise have to be remembered every time gets
enforced mechanically instead.

**think** — The slower path: reasoning something out in context rather than having a compiled
reflex catch it automatically. Warm memory tends to correspond to reflex-speed handling; cold
memory tends to require thinking it through.

**gate** — A check that a piece of work must pass before it is accepted, performed by a seat
distinct from the one that produced the work. The gate exists because a producer checking its own
output shares whatever blind spot produced the defect in the first place.

**tier (T1/T2/T3, OS_TIER, MOD_TIER)** — A ranking of which model is trusted to act with how much
supervision. T1 through T3 run from more to less capable/expensive under the orchestrator; MOD_TIER
is the moderator seat that sits above OS_TIER, which in turn sits above the numbered tiers — the
rule this enforces is that a cheap model builds and an expensive model gates, never the reverse.

**wrap** — The close-out step at the end of a work session: distill what was learned into atoms,
write them to the bank, and update a short summary index that the next session reads first. A wrap
that only appends instead of consolidating its own index will eventually degrade the index it is
supposed to maintain.

**relive** — Reconstructing what happened in a past session from its stored arc-cards and atoms,
without having the original transcript, in order to pick work back up or explain a past decision.

**harness** — The surrounding program that runs a language model as an agent: reading files,
calling tools, managing the session, as distinct from the model itself. The same model produces
different agent behaviour under different harnesses, because the harness and not the model decides
what state persists, what is injected at boot, and when a session ends. Harnesses often keep their
own conversation cache, which is a hazard: continuity supplied by a harness cache looks exactly like
continuity supplied by the bank until you change machines.

**hook** — A point in the harness's own lifecycle (for example, before or after a tool call, or at
session start) where a reflex or other automated check can be attached and run without the model
having to invoke it explicitly.

**cartridge** — A named, loadable bundle of capability or context that can be equipped for a
specific goal, distinct from a general-purpose model weight patch: a cartridge is retrieved and
applied at the harness/prompt level, not trained into the model.

**room** — A shared workspace tied to one project or campaign where multiple agents and the owner
post updates, rulings, and status, so state about ongoing work is visible in one place rather than
scattered across separate private sessions.

**boundary-driven** — A way of organizing work into four layers with one job each: a door that
holds no logic, a host that routes actions by reading declarative wiring, packages that each do one
task behind a versioned interface, and wiring files that hold paths and settings instead of code. A
package counts as done only when its own test suite passes against its declared interface.

**seat** — One model context, launched separately, holding only what its brief gives it. Two seats
may run the same model and still be independent, because neither can see the other's reasoning. The
unit matters because gating requires a seat that did not produce the work: a producer re-reading its
own output shares whatever blind spot produced the defect.

**receipt** — A logged record of an act the system actually performed: a tool call or a test run,
carrying identifiers, and re-runnable by someone else. A receipt is the difference between "this was
done" and "this was claimed"; to check one, you re-run the named command or test id against the same
branch and see whether the pass/fail agrees.

**body** — The full text of one stored lesson, as opposed to the one-line spine that recall shows.
A body is served only through the fetch door.

**spine** — The short, free surface of an atom: its title line and a preview, enough to decide
whether the body is worth fetching. Recall returns spines; it never returns bodies.

**impression** — A record that an atom surfaced in a recall result, distinct from a record that it
was used. Impressions are what make a take-up rate computable: without counting what surfaced and
was ignored, a fetch count is only a popularity number.

**born neutral** — The rule that an atom enters the bank at a fixed starting score its author cannot
choose or argue for. Every atom starts at the same value, so ranking can only encode what happened
after writing, never how emphatic the writer felt while writing.

**effective score (two surfaces)** — There is not one weight but two, and they can disagree. The
*stored* score is a column in the bank, moved by fixed constants when an event is witnessed. The
*recomputed* score is derived at read time from a history of deltas, and is what warmth reads.
Promotion candidates read the stored one. Neither is declared canonical, so anyone reimplementing
the ranking has to choose.

**fire_lower** — The verb that pushes an atom's score down by hand after a reader was misled by it.
It is deliberately asymmetric: there is no matching verb to push an atom up, because that would be
the author voting for their own memory again. Lowering decays the score toward the neutral anchor
and never deletes the atom.

**hand-path** — Any change to an atom's standing made by a human or agent deciding to make it,
rather than by the engine observing an event and recording it. `fire_lower` is the only hand-path in
the scoring model, and the fact that it runs one way is the whole design.

**disclaimed / disputed.** One state, two words in the record: a human marked the atom as wrong or misleading. Its score is pinned at the disclaim floor (75 on the internal scale) and it leaves the default recall view. It is never deleted and can be re-earned.
