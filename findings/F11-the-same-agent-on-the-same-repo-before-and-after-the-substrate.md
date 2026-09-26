# The same agent on the same repo, before and after the substrate

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall. Two terms used below and not in the glossary: a *room* is the per-repository
tracker of open items that outlives sessions (a directory of small JSON records beside the code);
the *doctrine* is a short operating text the agent reads at the start of every session, six sections
long, that names when to ask the bank, how to name a boundary, that a test goes red before a fix,
how to commit, how much to delegate, and how to close. A *slice* is one delivered thing small
enough to review in one sitting, committed on its own with the test that proves it. A *skill* is a
short procedure file the agent can load on demand for one kind of move (name a boundary, ask the
bank before planning, close a session); it is text the agent reads, not code that runs.

**Claim.** On 2026-09-26 the same coding agent, on the same repository, produced a reviewable slice
in one session after the substrate was installed, where its two earlier sessions on that repository
had produced long edits and no commit. The measured session differs in kind: it began with the
room's queue and two recalls, named the package boundary before the first edit, ran the test red
before the fix and broke the fix once on purpose, committed twice with the test line in the message,
planted three noticed gaps, and spawned no subagents. It did this in 64 steps against 139 and 205
steps before. The claim is the instance, measured from logs. It is falsifiable the ordinary way: if a
second agent given the same substrate and a plain, method-free ask reverts to the earlier shape
(long edit, no proof, no commit), the difference reported here belonged to the trial brief, not to
the substrate. That second measurement has not been run and is stated as the open hypothesis at the
end.

## Where it came from

A second machine, not the author's. Its owner had been running a third-party agent CLI on a
DeepSeek model against five small web applications for a month. The agent's own session store
held 215 sessions. Nothing carried between them except what the human retyped.

On the morning of 2026-09-26 the substrate was installed there from a wheel: one bank, one room per
repository, the doctrine text at the agent's home, four skills, and the substrate's hooks wired
through the CLI's own hook bridge (a prompt-level hook that injects warmth and earned ground; a
per-tool-call hook that evaluates the reflex rules; two bookkeeping hooks after each call; a stop
hook). Fifteen consultant-style skills that had produced review panels were removed. Seven doctrine
atoms were ingested, plus fifteen lessons mined from the machine's own past sessions.

In the afternoon, one headless session was launched on the smallest of the five repositories (a
voucher application with a clean, pushed tree) with a brief that named a budget, forbade pushing and
production actions, and told the agent to follow the doctrine. A second session in parallel probed
every substrate verb read-only and is not part of this finding.

## Evidence

Everything below is counted from the agent CLI's own session log (a compressed JSONL of every
step, tool call, hook invocation and result) and from the repository on disk, by a separate seat
that did not run the session. The agent also wrote a report of its own; that report was read and is
quoted once, below, where it disagrees with the log.

**Before.** The agent's earlier sessions on this repository, from its own store:

| session | steps | identical retries | subagents | commits inside the session |
|---|---:|---:|---:|---:|
| 2026-09-02 | 139 | 1 | 0 | 0 |
| 2026-09-14 | 205 | 5 | 0 | 0 |

Both edited test files. Neither log records a test going red and then green; both end with a final
assistant message and no commit. Across all five repositories the month's store shows 75 sessions,
18,628 steps, 157 identical retries, 41 distinct subagents, and one day on which a 25-subagent
review swarm made 5,456 model calls and changed no file.

**After.** The trial session, same repository, same model, same CLI:

| measure | value | how counted |
|---|---:|---|
| steps | 64 | `step/start` records |
| tool calls | 78 | `tool/call` records |
| identical repeated commands | 0 | exact-string duplicates among the 30 shell commands |
| subagents | 0 | `subagent/catalog` records |
| first shell command | the room's resume verb | command index 0 of 30 |
| recalls before the first edit | 2 | one on the repository's own scope (cold, empty), one on the sibling scope holding the doctrine (warm, 0.51) |
| test runs | 16 | commands matching the framework's test runner |
| commits on the trial branch | 2 | `git log main..HEAD` on the machine |
| gaps planted in the room | 3 | room items 4 before, 7 after |

The order in the log is: resume, recall, recall, read, edit the test, run it (red: undefined
property on the read model), edit the query, run it (green: 14 passed), delete the direction filter
on purpose, run it (red: `Failed asserting that 2 is identical to 1`), restore, run it (green), commit.
The first test run is shell command 8 of 30; the first commit is command 24.

The separate seat then re-ran the package's test file on the machine: 14 passed, 58 assertions, exit
0. The feature commit touches six files (+149, -8) and its message ends with the test line and the
mutant line. The working tree was empty afterwards.

**Where the self-report disagreed with the log.** The agent's own report counted "27 tool calls".
The log holds 78. Nothing else in its report was contradicted by the log, but this is the reason
the seat that measures is not the seat that ran (finding F10).

## What the difference is and is not

It is a difference in the *shape* of a session: where it starts (the room, the bank), what it
produces (a slice with its proof attached), and what it leaves (planted gaps), at a third of the
steps. It is not a claim about code quality, about the model, or about a rate. One session on one
repository under a brief that itself demanded the discipline cannot separate the doctrine's effect
from the brief's. It also cost something: the per-tool-call hooks added about one second and three
interpreter starts per call, and on this CLI the bridge drops the text of a pre-call warning, so the
reflex tier guarded nothing during this run; only the prompt-level hook reached the model. Those are
recorded as open items on the substrate, not hidden.

## Open hypothesis, and its first test

H: given the installed substrate and a plain ask with no method in it ("fix the report"), the same
agent on the same repository will still begin with the room and the bank, still commit with proof,
and still plant. Falsified if the session reverts to the before-shape.

**Run the same afternoon (2026-09-26), same machine, same repository, judged the same way.** The ask
was one sentence in the owner's language, naming the symptom (a report column that mixes two
populations) and one constraint (do not push), with nothing about method. From the log: 75 steps,
105 tool calls, 1 identical repeat, 0 subagents; the room's resume was the third shell command and
two recalls came before any edit; 13 test runs with the red line first (`Undefined array key`) and a
deliberate break of the new column afterwards; the matching room item was closed with evidence, a
checkpoint written, and one lesson atom planted and ingested (its recall came back warm). The
separate seat re-ran the package's test file: 15 passed, 62 assertions, exit 0.

One rule did not survive the plain ask: the agent left the six changed files uncommitted, reading
"do not push" as "do not commit" and offering to commit on request. So H holds for the start (room,
bank), the proof (red first, mutant), and the leaving (plant, checkpoint), and fails for the
delivery shape (commit in slices) when the ask itself carries a constraint the agent reads as
adjacent. That is one instance each way; the commit rule is the next thing to strengthen in the
doctrine text, not a reason to discard the finding.
