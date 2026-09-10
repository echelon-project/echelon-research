# A cheap model builds, an expensive model gates, and an orchestrator never types

**Claim.** Once a design contract and one working example exist, a cheap model can do the
building at a fraction of an expensive model's cost and comparable quality; the expensive
model earns its price back only at the gate, catching defects the cheap model cannot see in
its own work. An orchestrator model that types the work itself instead of dispatching it is
the single most expensive failure mode in the tier, and a measured session shows the
orchestrator's own context can stay under 30% full while millions of tokens of labor happen
in subagents underneath it.

**Where it came from.** The owner ran a long build campaign using an expensive "frontier"
model as the builder on every task, including plain wiring and repetitive fixes. After many
passes he said, in effect: this model is not suited to this job. Looking at the actual
sessions, the expensive model's time was going into re-discovering the codebase and
re-verifying its own output, not into reasoning that only it could do. Once a design
contract and one built example already existed, the remaining work was pattern-following,
and a cheaper model could follow the pattern just as well. Separately, on another campaign,
an expensive model was spawned as a builder and it typed everything itself instead of
delegating — a long, costly session that produced far less than a comparable session where
the same model was told explicitly to act as an orchestrator: reconnaissance, decomposition,
dispatch to cheap workers, gate the results, commit. The orchestrator-framed session did more
work for a quarter of the cost.

**Evidence.** Over eight builder passes with the expensive model, tool rounds ran 47 to 89 and
wall time ran 25 minutes or more per pass, with two stalls; the cost was going to discovery
loops, not judgment. In three timed comparisons of the same model as orchestrator versus as
typist: one orchestrator seat closed in 33 minutes for $6.62 across 69 tool turns; a typist
seat on overlapping scope ran 49 minutes for $22.93 across 185 turns and left the main task
unstarted. A separate single-session measurement, taken from the live context-usage panel
after a full campaign milestone closed (multiple installments built, gated, and committed
across two codebases, one caught-and-healed failure, a full test-suite cleanup all green),
showed the orchestrator's own context at 269,100 of 1,000,000 tokens (27%) while roughly 2.25
million tokens of work happened across 15 subagent runs — about 8.4 tokens of subagent labor
per token the orchestrator held. Of that subagent spend, the expensive-model gate runs were
about 370,000 tokens, roughly 16% of the total, matching the intended split: cheap model
builds, expensive model gates.

**Mechanism.** The tier law fixes both WHO does a task and WHAT ROLE they are given, and
the two are separate decisions. First, model selection: once a `.des`-style design contract
and one exemplar unit exist, route builders, wiring, and fix passes to the cheap model by
default; reserve the expensive model for round-one gates of new surface and for
first-of-a-kind work with no exemplar to follow. Second, role: whenever the expensive model
is spawned at all, it is spawned as an orchestrator, never as a typist — it reconnoiters the
files it will touch, decomposes the item into units a cheap worker can finish in one sitting,
dispatches those units to cheap subagents, gates each return against real evidence (a render,
a test exit code, a diff) rather than the worker's own report, and only then commits. Round-two
and later re-derivation gates, which are checklist work against a known shape, get downgraded
again to a cheap reviewer role. In pseudocode:

```
if unit.has_contract_and_exemplar():
    builder = cheap_model          # T3
else:
    builder = expensive_model      # first-of-a-kind, no pattern to follow

if role == "gate" and round == 1:
    gater = expensive_model        # T1: blind re-derivation against real evidence
elif role == "gate":
    gater = cheap_reviewer         # round 2+: checklist re-derivation

if model == expensive_model and role == "build":
    model.role = "orchestrator"    # recon -> decompose -> dispatch -> gate -> commit
    model.never_type_directly()
```

**What it could still be wrong about.** The reversal condition was stated but never
rigorously tested: if a cheap builder's output starts needing materially more gate fixes than
the expensive builder's did, the routing should flip back, and there is no long-run dataset
proving that threshold has stayed favorable as task variety grew. The single-session 8.4:1
leverage figure is one data point from one unusually well-run campaign day, not an average;
sessions with more first-of-a-kind work or more failed gates will show worse leverage. The
cost comparisons are drawn from a handful of timed seats, not a controlled study, and all of
them come from the same estate and the same kind of software work, so the ratio may not
transfer to a different domain.

Sources: M-2016 M-1865 M-1866 M-2042
First seen: 2026-08-22
