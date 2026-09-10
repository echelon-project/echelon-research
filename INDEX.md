# ECHELON research release v0.1 — contents

Start with [THESIS.md](THESIS.md) (one page). Then the findings in order; each stands alone.

## Findings
1. [Identity does not transfer by injection](findings/F01-identity-does-not-transfer-by-injection.md)
2. [A session boundary is a transition, not a failure](findings/F02-a-session-boundary-is-a-transition-not-a-failure.md)
3. [Memory lives outside the model, append-only](findings/F03-memory-lives-outside-the-model-append-only.md)
4. [A memory is a weight-adjustor, not a record](findings/F04-a-memory-is-a-weight-adjustor-not-a-record.md)
5. [Weight is earned by trace, born neutral](findings/F05-weight-is-earned-by-trace-born-neutral.md)
6. [Recall is foveated; demote, don't delete](findings/F06-recall-is-foveated-demote-dont-delete.md)
7. [Pull recall cannot ask what it does not know](findings/F07-pull-recall-cannot-ask-what-it-does-not-know.md)
8. [The bank remembered for the human first](findings/F08-the-bank-remembered-for-the-human-first.md)
9. [Weights cannot hold it: LoRA facts recall, skills memorise](findings/F09-weights-cannot-hold-it-lora-facts-recall-skills-memorise.md)
10. [A generator validating itself shares its blind spot](findings/F10-a-generator-validating-itself-shares-its-blind-spot.md)

## Methods
- [Tier law and the token economy](methods/MT1-tier-law-and-the-token-economy.md)
- [Reflex vs think](methods/MT2-reflex-vs-think.md)
- [Wrap, arc-card, relive](methods/MT3-wrap-arc-card-relive.md)
- [Grounding against the live system](methods/MT4-grounding-against-the-live-system.md)
- [Boundary-driven work map](methods/MT5-boundary-driven-work-map.md)
- [Bank sync and measurement traps](methods/MT6-bank-sync-and-measurement-traps.md)

## Appendix
- [AP1 Timeline: every law has a birthday](appendix/AP1-timeline.md)
- [AP2 Retractions](appendix/AP2-retractions.md)
- [AP3 Glossary](appendix/AP3-glossary.md)
- [Public claims ledger](_ledger/claims-public.jsonl) (the `M-####` ids cited in the findings; claim, kind, date, status, topic)

## How this was produced
Mined from five months of private operating records, rewritten for a reader outside the project,
each finding read cold by a reviewer who had never seen the system and revised against that verdict.
The private archive and its source paths are not published. The verdicts are: [_gate/verdicts](_gate/verdicts/).

The code is at [echelon-project/echelon](https://github.com/echelon-project/echelon) (Apache-2.0).
