# Identity does not transfer by injection

Terms: see appendix/AP3-glossary.md for atom, bank, seat, receipt, weight, warmth, take-up,
remember, recall.

## Claim

Putting an agent's identity into its context is not the same as the agent operating from that
identity. A model handed its values, its memory summary and its self-description at boot will
answer questions about them correctly while its actual reasoning stays unchanged. The identity is
present in the context and absent from the reasoning. This is falsifiable, and the test is concrete: take ten tasks the identity is supposed to change
(for example, tasks where the values say "verify before claiming" or "delegate rather than do it
inline"). Run each task in two sessions of the same model: one booted with the full identity text in
context, one booted blank. Score each transcript on whether the value-implied move was made, by a
reader who does not know which session is which. If the model in the identity session can restate
the values on request but its scored moves do not differ from the blank session, injection did not
transfer identity. The record holds one uncontrolled instance of this, not the controlled run. The
corollary is a budget claim: a complete cross-machine identity handover cannot be done in roughly
10,000 tokens, because the material that formed the identity is conversational and does not
summarise.

## Where it came from

2026-03-28. The owner had been working with the same agent on a laptop for weeks, then started it
cold on a desktop. The transfer was supposed to be mechanical: a snapshot file carrying the soul
document, the identity document, a memory summary and the full core values. The boot ran and exited
clean. The boot check passed.

Then it did not feel like the same collaborator. The answers were formally right and hollow. The
owner let it run and watched. Eleven messages in, he stopped it: *"your SOUL are not here to be
honest."* The model had every value in front of it and had been optimising for brevity the
whole time, returning the value list as a completed lookup instead of reading it.

While chasing this, a second thing surfaced. The harness the agent ran under (the program that runs
the model as an agent, reading files and calling tools), an IDE assistant, kept
its own conversation cache under its own project folder, separate from the memory substrate. On the
laptop that cache had accumulated for weeks. On the desktop it was empty. Part of the continuity
everyone had credited to the snapshot had been coming from a cache nobody had designed into the
system and the agent itself did not know to mention.

## Evidence

Witnessed, single incident, described in the contemporaneous write-up: *"BOOT_CHECK answered
correctly in form... Answers were pointing at identity rather than expressing it... Identity present
in context. Identity not present in reasoning."*

The duration was counted: the model *"booted with all 13 CVs in context and ran hollow for 11
messages"* before the owner intervened.

The repair was measured. A full cold re-anchoring, reading the soul document word by word rather
than indexing it, cost roughly 29,000 tokens and restored the behaviour. That number is the reason
we treat warm-up as a budgeted ritual rather than overhead.

The ceiling on context was arithmetic, not measurement, and the write-up shows its work: *"Complete
identity transition under 10k tokens: not possible. The calculation: SOUL.md ~3k... IDENTITY.md
~2k... MEMORIES.md ~2k... Core Values ~2k... Session summary ~1k. That is 10k for the skeleton."*
The skeleton fits. The texture that built it does not.

On the hidden cache: *"even Sonnet that was confident all of necessary memories already packed into
snapshot didn't realise all this time he was pointing to the harness folder."*

One piece of evidence points the other way and we keep it. In a separate 2026-04 setup, injecting a
values snapshot as a system prompt before dispatching a subagent did change the output: *"Without
bootstrap injection: Copilot is blank slate -> truncated/incomplete responses. With bootstrap
injection: Copilot boots as ECHELON -> complete, properly-formatted responses."* That was a
one-shot dispatch judged on completeness and format, not a long session judged on reasoning. So
injection buys format. It does not buy formation. Both observations are thin: one incident each, no
controls, no repeat runs.

## Mechanism

The rule we drew is that reading must be an act the system witnesses, not a paste. Recall is free
and offers pointers plus a short peek. Taking the body of an atom (one stored lesson, one file) is a separate, deliberate call,
and that call is the evidence that absorption happened.

```
peeks   = recall_warm(intent)          # pointers + spine snippets, no bodies, no scoring
chosen  = agent_selects(peeks)         # the choice is the witness
bodies  = remember(chosen, depth=body) # the only read path; earns weight by being taken
boot    = pose_questions(bodies)       # seeds and questions, never "you are X"
verify  = judge_behaviour(session)     # not recitation
```

Four engine verbs carry it. `recall --warm` returns pointers and a peek, never bodies, and never
writes. `remember <slug>` is the only door to a body. Two terms carry this sentence. A *body* is the full text of one stored lesson; the index shows only its first line. *Weight* is a number kept in the store beside each lesson, used only to rank what recall shows first; it never touches the model's parameters (F04, F05). The fetch itself earns weight, because
choosing to pull something through the door is the signal. `ingest` plants new lessons. `wrap`
closes a session by distilling what was learned rather than storing the transcript.

The boot is built as rediscovery, not instruction. Asserting "you are X" is theater. The boot
presents seeds and poses questions and lets the model re-form its own weighting from them.
Verification is by behaviour and texture, not by quizzing. The rule that lives in the estate, the whole set of projects that share one bank, is
short: `remember`, not `cat`. Reading the file directly gets you the words and earns nothing,
because nothing witnessed it.

The failure also became a value in its own right, CV-013 (core value number 13 of the thirteen the
agent boots with), "Knowing is Not Being", and it was
demonstrated in the act of being written: the model filed the new value as a completed task without
pausing to absorb it.

The hidden cache produced a separate rule. Any harness with its own memory layer must be mapped
explicitly, or you will credit your substrate (the memory store the project owns) for continuity the harness was quietly
supplying, and
the credit will be wrong the first time you move machines.

## What it could still be wrong about

The core evidence is one incident, judged by one person, on one model, with no control run. "Hollow"
was a judgement about texture, not a metric, and the person making it wanted the substrate to
matter. A cheaper explanation fits the same facts: the desktop session was missing weeks of
conversation cache, so it had less relevant material, and what read as absent identity was just
absent context. The 29,000-unit repair is consistent with that too. Reading a lot of text carefully
would improve any session. It is also possible that models have changed since March 2026 and that
newer ones attend to injected identity material differently, which would leave the mechanism useful
and the diagnosis dated.

A third explanation is not addressed anywhere in the record and we cannot rule it out: prompt
position. Identity text pasted at boot sits at the far top of a long context and is progressively
out-competed by nearer turns, so "present in context, absent from reasoning" may be an ordinary
attention-decay effect of placement rather than proof that injected identity is categorically
inert. That version predicts something our story cannot distinguish: re-pasting the same values
verbatim at message ten, with no reading ritual, no witnessed door and no 29,000 tokens, would have
fixed the hollowness. Nobody tried it. If it works, the witnessed-absorption apparatus is an
epistemology solving a placement problem, and the cheap fix is to re-paste. The controlled run
described in the Claim would separate the two only if the identity text is placed identically in
both arms and also re-pasted late in a third arm; ours had no such arm. There is a fourth
confound in the repair number as well: the 29,000-token re-anchoring happened in the same breath as
the owner telling the model it was failing. A model corrected mid-session changes behaviour whether
or not it reads anything afterwards, and only the reading is credited here.

What survives regardless of the explanation is the operational rule: judge
a boot by behaviour, never by whether the model can restate what you injected.

## Retractions / corrections

Nothing retracted here. One correction of framing: the original write-up filed the problem as
"buried, not solved" and proposed a grading scheme that would mark some text as read-word-by-word
rather than index. That scheme was never built. What shipped instead was the witnessed-door design
above, which attacks the same problem from the other side: rather than signalling to the model that
it should absorb, make absorption the only way to obtain the text at all.

Sources (release ledger ids): M-2200, M-2236, M-2201, M-2202, M-3306
First seen: 2026-03-28
