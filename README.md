# ECHELON public research release (working tree)

**Thesis (owner, 2026-09-10):** this work began as a question about continuity, not capability:
how does a language model with a bounded context window keep remembering, and stay itself, across
a working relationship that has no end? The first months went into how context and memory actually
behave, then into preserving the model's identity across sessions; the harness memory files and the
gap between a growing memory and a small window were the pilot. Token economy, gates and the
discipline that lets cheap models act like expensive ones were engineered afterwards, because
continuity cannot be afforded without them. They are chapters. Continuity is the title.

**Reader:** someone who works with a language model over months and wants it to keep remembering
and remain the same collaborator, given a bounded context; an engineer by trade, reading a technical
report they can act on in one sitting.

**Genre:** technical report + one md per finding + a repo a stranger can run in ten minutes.

**Source:** a private archive of five months of operating records (never published).
**This tree:** what a stranger sees. Nothing enters without passing `_gate/redact.py`.

## Layout
- `_ledger/claims-public.jsonl`  every claim cited by the findings (id, claim, kind, first_seen, status, topic)
- `_ledger/SCHEMA.md`      the row shape and the status vocabulary
- `findings/NN-<slug>.md`  one finding per file, written for the reader, evidence inline
- `methods/`               mechanisms (memory-as-weight-adjustor, foveated recall, reflex vs think,
                           tier law, gate laws, boundary-driven, arc-cards, harness mirror)
- `hypotheses/`            claims without a witnessed evidence line (stated as open)
- `appendix/`              timeline (every law has a birthday), retractions, glossary
- `_gate/`                 redaction scanner + the zero-context skeptic brief
- `THESIS.md`              one page

## Cut law
v0.1 = THESIS + 10 findings + methods + timeline. Ceiling for the whole report: 30 findings.
Retractions stay in. Client names, people, credentials, customer data: never.
