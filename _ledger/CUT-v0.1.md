# v0.1 cut (Fable seat, 2026-09-10) — the continuity spine

Order follows the owner's thesis: continuity first, mechanism second, what could not work third,
then the economy that pays for it. Claim ids refer to _ledger/claims.jsonl (mid).

## Findings (10 for v0.1)
F01 identity-does-not-transfer-by-injection          | M-2200 M-2236 M-2201 M-2202 M-3306   | 2026-03-28: values in context are pointed at, not acted from; ~10k tokens cannot carry a cross-machine identity; the harness cache did half the work undesigned
F02 a-session-boundary-is-a-transition-not-a-failure | M-3279 M-3273 M-3345 M-3274 M-3393 M-3337 | 2026-03-23..04-26: conclusions, not transcripts, rebuild identity; measured 175KB conversation -> ~631 ingest tokens in a 3-session comparison
F03 memory-lives-outside-the-model-append-only        | M-3272 M-3280 M-3281 M-3404 M-3248 M-3403 M-3394 | 2026-03-25: an external organ survives context wipes; content-addressed, append-only, supersedes pointers instead of edits; warm boot per dispatch
F04 a-memory-is-a-weight-adjustor-not-a-record        | M-2207 M-3189 M-3190 M-2260 M-2261   | 2026-06-05: recall = applying adjustors, one lesson per atom; honesty clause 2026-09-08: the weight is a selection score in a database, not a model parameter
F05 weight-is-earned-by-trace-born-neutral            | M-2397 M-3029 M-3192 M-3188 M-3028 M-3196 M-3109 M-2265 | born neutral (flat 100 internal scale; 0.31 was a normalised readout), earned only when a card that used it succeeds; peek is free, fetch is paid; reading the file directly earns nothing; a read must not score like an outcome
F06 recall-is-foveated-demote-dont-delete             | M-3191 M-3124 M-2526 M-2208 M-3053 M-3008 M-3031 M-3032 M-3052 M-2264 | warm/lukewarm/cold; lukewarm = one bounded probe; decay at read time with a floor and per-type rate; the normalisation bug that cancelled aging (2026-09-09)
F07 pull-recall-cannot-ask-what-it-does-not-know      | M-2226 M-2097 M-2098 M-2089 M-2109 M-2216 M-2227 M-2209 | 2026-08-02 a fact sat verbatim for months; the per-turn nerve; calibration 2026-08-25 (warmth predicts take-up); RETRACTION: the judge was never wired, 69% lexical floor; past-window control
F08 the-bank-remembered-for-the-human-first           | M-2121 M-2203 M-3384 M-2134           | 2026-09-04 the substrate warmed the owner's own memory; 2026-05-30 a compressed witnessed sentence recognised cold by another instance (resonance, three axes)
F09 weights-cannot-hold-it-lora-facts-recall-skills-memorise | M-2234 M-2205 M-2206 M-2204 | 2026-06-20..07-06: a 1.6MB patch recalls a narrow fact on untrained phrasings; a skill patch memorises; a stored fact stays invisible mid-reasoning -> why a store, not the weights
F10 a-generator-validating-itself-shares-its-blind-spot | M-3250 M-2236 M-2782 M-2043 M-2045 M-3275 | 2026-04-11 cheap models role-play pipeline output and fabricate results; 2026-08-15 gate seat != producer seat; verdict law CONFIRMED/PLAUSIBLE

## Methods (section, not findings)
MT1 tier-law-and-the-token-economy       | M-2016 M-1865 M-1866 M-2042 M-2100 M-3239 M-3240 | T1/T2/T3 first 2026-03-21; Sonnet builds Opus gates; orchestrator not typist; measured cost datum; brevity as policy
MT2 reflex-vs-think                      | M-2170 M-2126 M-1986 M-1990 M-2548 | compiled guards fire pre-tool; fires grew 8.2x while verbs stayed flat, ~70% spurious -> demotion by evidence; familiarity moves downward
MT3 wrap-arc-card-relive                 | M-2014 M-2132 M-2131 M-3131 M-3367 | lessons bank midway; STOPPED-UNWRAPPED reachable; index size gate; lessons vs operational state; delta line on every stop
MT4 grounding-against-the-live-system    | M-2525 M-2771 M-2712 M-2587 M-2769 M-1980 | docs from uploads invent mechanisms; three successively cheaper passes; ship when the next gap is invisible from inside
MT5 boundary-driven-work-map             | M-1789 M-1826 M-2085 | door/host/wiring/packages; freeze is a boundary not a binary; the tracker row is the root
MT6 bank-sync-and-measurement-traps      | M-2293 M-2301 M-2755 M-2605 M-2212 M-2243 M-2296 M-2962 | replay events not scores; journal was 68% of the bank; non-unique join keys; keyword sweeps overstate; WAL copy stub

## Appendix
AP1 timeline: every law has a birthday (dates above; DOME -> ALPHA_DOME -> ECHELON OS -> ECHELON; EROS layer-zero thesis M-3402)
AP2 retractions kept: judge never wired (F07); two-band temperature model withdrawn (M-2783); v1 judge law over-applied (M-2782); normalisation cancelled aging (F06)
AP3 glossary

## Ceiling
30 findings for the whole report; v0.1 ships 10 + THESIS + methods + timeline.
