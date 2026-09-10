# A compiled guard fires before the tool runs, so the model never has to remember the rule

**Claim.** Rules that would otherwise live only as prose the model has to recall and reapply
every turn can instead be compiled into pattern-matched guards that fire automatically before
a matching tool call executes, catching the mistake without spending a reasoning turn on it.
This works, but a guard's reach must be scoped as tightly as its pattern is generic: a rule
declared global with a broad pattern will fire on unrelated work far more than a scoped rule
ever would, and the excess fires are pure noise that bury the guards worth reading.

**Where it came from.** Two failure shapes showed up in the same system on the same kind of
day. First, worker sessions doing throwaway bench work (building fixture repos to test
something else) kept tripping guards that belonged to entirely different projects — a rule
meant to check secret handling on one project, a rule meant to verify payload provenance on
another, both firing on fake data that had nothing to do with either project. Second, a
separate audit was asked why cross-project noise persisted after a supposed cleanup, and
found the cleanup had fixed the wrong axis: it re-checked which project each rule was scoped
to, but never checked whether the rule's matching pattern was specific enough to deserve
running against every command on the whole machine. A rule scoped "global" with a pattern as
broad as "any recursive search" or "any git push" will match constantly, regardless of
project.

**Evidence.** One measured session window recorded 170 guard fires total, and the noisiest
individual guards were all foreign-project checks tripped by disposable fixture work: one
project's provenance-check fired 27 times, another project's secret-verification check fired
25 times, a third project's payload check fired 9 times — none of their actual trigger
conditions were present. Separately, an all-time fire count showed one overly-generic
global-tier rule (matching any recursive grep) had fired 1,182 times, three times noisier than
any other guard on the system. A prior audit of the same rule set found 63 of 147 compiled
rules carrying no explicit scope tag; that turned out to be cosmetic, since those rules
already defaulted to their own project's scope at fire time. The real source of cross-project
bleed was rules correctly marked global whose patterns were too broad for that reach. Guard
compilation is also scoped per project — one compile run replaces the rule set for one project
only — so a rule change made in one project's compile does not reach the others until each is
recompiled separately, a second, distinct source of drift.

**Mechanism.** A guard is a small pattern-matched rule compiled from natural-language intent
into a structural check that runs in the pre-tool-call hook, before the tool executes, so it
costs no reasoning tokens on clean turns and blocks or warns on the turns where something is
wrong. Compilation is distinct from writing the rule down: prose lives in memory as a recalled
atom; a reflex is that atom's condition turned into a matcher the harness runs mechanically.
Scope and pattern specificity are separate axes, judged independently: a rule scoped to one
project stays fenced even without an explicit tag (it defaults to its own scope), but a rule
promoted to fire everywhere is held to a stricter bar — would this pattern trip on a command
from a project it has never touched? If yes, it is too broad for global reach even with the
correct scope tag. In pseudocode:

```
def compile_reflex(rule):
    pattern = rule.condition_as_regex()
    scope = rule.get("tier", DEFAULT_TIER)          # defaults to the compiling project
    if scope in ("global", "portable"):
        assert pattern.would_not_fire_on_unrelated_project(), \
            "pattern too generic for machine-wide reach"
    return CompiledGuard(pattern, scope)

def on_pre_tool_call(cmd, cwd):
    for guard in compiled_guards:
        if guard.scope_matches(cwd) and guard.pattern.search(cmd):
            fire(guard)   # warn or block, before the tool runs
```

A guard that fires thousands of times is itself a signal: high-frequency, low-judgment firing
marks a check that should become a deterministic pre-check or a rewritten tool, not a standing
warning the model reads past every time. The same principle appears in a separate design note
on running an agent loop past its context limit: rather than treating the limit as a hard stop
needing an external resume token, the loop compresses its own state into a short persistent
summary, the noisy transcript is discarded, and the loop re-enters on the summary alone — the
same move as a reflex, applied to a whole session instead of one rule: push recurring judgment
out of the part that has to be re-reasoned every time, into a small compiled or compressed
artifact a cheaper mechanism can carry forward.

**What it could still be wrong about.** The 170-fire measurement and the 1,182-fire count are
each a single snapshot from one system's history, not a controlled comparison, so the
noise-to-signal ratio they imply may not generalize to a system with different rule counts or
different worker patterns. The fix proposed — scope-gating fires to the project the working
directory belongs to, plus per-rule exclusion patterns — was written up as a plan, and this
packet does not carry evidence that it was implemented and re-measured, so the claim that
tightening the pattern axis actually reduces noise (rather than just relocating it) is
inferred, not witnessed twice.

Sources: M-2170 M-2126 M-2548
First seen: 2026-08-12
