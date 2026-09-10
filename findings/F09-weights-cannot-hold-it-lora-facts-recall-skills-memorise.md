# The weights can hold a fact, but not a skill, and not a fact your reasoning can reach

**Claim.** If you want a model to keep remembering across months, you cannot get there by
writing the memory into the model's weights, at least not at a budget any individual can afford.
A small weight-patch can hold one narrow fact and recall it with no prompt at all, on phrasings
it was never trained on. That much is real and measured. But two things break. A patch trained
on a procedure memorises its training examples instead of learning the procedure, and it damages
the model's ordinary language while doing so. And a fact stored in a patch is a route, not
knowledge: the model will answer a training-shaped question with it, and then fail to use the
same fact three steps into a piece of reasoning. So the memory has to live outside the model, in
a store the model reads at the start of a turn. That is the whole reason ECHELON is a bank and a
recall verb rather than a training loop.

**Where it came from.** Between 2026-06-17 and 2026-07-06 the owner ran the question directly
instead of arguing it. The design papers of the estate had a standing claim: save the parameter,
not the context. If a fact is a weight, you never pay to re-feed it. The experiments were built
to try to prove that claim right, on a consumer machine, in evenings. A small open model
(SmolLM2-360M-Instruct, later a 1.7B sibling) was patched with LoRA adapters on a desktop GPU.
The first experiments were about a single fact: the model's own name. The last ones were about a
skill: a seven-criterion audit procedure the estate had already earned, taught to the patch from
351 real judgment traces. The order matters. The cheap, encouraging result came first. The wall
came second, and the wall is what changed the architecture.

**Evidence.**

Fact, real silicon, 2026-06-20. EXP-0026-c: SmolLM2-360M, a 1.6MB LoRA trained on one fact
("your name is ECHO") mixed with a handful of neutral question/answer pairs. Booted with zero
context and no system prompt. The unpatched control said its name 0 out of 5. The patched model
said it 5 out of 5 on five phrasings that were never trained ("What should I call you?" ->
"You are called ECHO"). False-fires 0 out of 3: asked the capital of France it said Paris. The
whole identity fact was 1.6MB on disk. A first run at a stronger dose (r=8, alpha=16, 40 epochs,
no neutral examples) generalised equally well but false-fired 3 out of 3, answering "My name is
ECHO" to the capital of France. Dropping the dose (r=4, alpha=8, 25 epochs) and mixing in
neutral examples fixed it. Note for the reader: the often-quoted companion number, a rank-1
patch generalising 12 to 64 percent on unseen phrasings where "a pure lookup would generalize
0%", is EXP-0026-b, which ran on 300 *toy* models with random mean-pooled embeddings, not on a
transformer. It is a mechanism probe, not a result about an LLM. The real-silicon result is the
5/5.

Skill, 2026-07-06. EXP-0026-j: LoRA r=16, alpha=32, 3 epochs, 341 training traces and 10 held
out, on the 360M console. Train loss fell from 4.06 to 0.33, so the patch absorbed the mapping
completely. On the 10 unseen surfaces the output format survived 1 out of 10, and the criterion
score was 0.71 against a 0.99 baseline. The verdict in the write-up: "Low train loss + no
transfer = lookup table." A separate control asked three neutral questions. The patch did not
blurt verdicts, but all three answers degenerated into a repeating attractor. The patch had
overwritten general behaviour rather than writing a skill beside it.

Composition, the same night. EXP-0026-k tried the owner's split: facts in the weights, procedure
in the prompt, reasoning composes them. At 360M the model's priors beat the patched values. At
1.7B, twelve epochs, the patched facts came back verbatim 2 out of 3, and composition, using the
stored fact inside a reasoning chain, fired 1 out of 6. The recorded finding: "a patched fact is
a memorized ROUTE, not integrated knowledge, retrievable by a training-shaped question, invisible
to reasoning mid-procedure... Context recall remains the only reliable composition mechanism."

The boundary, 2026-06-17. A related attempt transferred a capability to a weak frozen model as
an earned move-cartridge. The moves fired and the graph edges were valid, so the discrete "which
move to make" part transferred. But the model still dropped load-bearing facts, because faithful
compression is execution skill, not a move, and nothing was earned (warm 0 of 21). A capability
splits into a move, which is storable, and an execution skill, which stays entangled in the
frozen weights.

**Mechanism.** Because of these results ECHELON keeps memory as text outside the model and pays
a re-feed tax on every turn instead of a training cost once. A lesson is written as one markdown
atom, planted with `ingest`, and retrieved at turn start with `recall --warm`, which scores
candidates for warmth against the current intent and returns a small foveated set: warm bodies
inline, colder rows as one-line titles. `remember <slug>` pulls a full body when the model
decides it needs it, and reading it raises that atom's weight. `wrap` distills a session into new
atoms. In five lines:

```
atoms   = load(bank)                       # text, not weights
warm    = topk(score(atoms, intent), k)    # recall --warm
context = render(warm) + render_titles(rest)
answer  = frozen_model(context + prompt)   # weights never change
bank   += distill(session)                 # wrap, then ingest
```

The re-feed tax is not overhead. It is what buys composition, which the patch could not do.

**What it could still be wrong about.** Every number here comes from weekend-scale budgets: a
360M and a 1.7B model, one consumer GPU, one LoRA configuration each, three epochs on the skill
run, inputs truncated to 2,600 characters because the machine ran out of memory at 6,000. The
estate's own dosage rule suggested r >= 1.6N for facts, and a skill spread over 341 diverse
traces at r=16 was far under any plausible dose. So the honest scope is: at this height the wall
is real. A larger console, a dose scaled to the content, cleaner or fewer traces, or a curriculum
could each move it, and the 1 out of 6 composition flicker at 1.7B reads more like a weak flame
than a hard ceiling. The conclusion that survives is about economics as much as physics. A store
you can write to in a second beats a patch you must retrain, and the patch route was measured,
not assumed.

**Retractions / corrections.** The evidence line as originally packeted cited the 12 to 64
percent generalisation figure alongside the real-silicon result, implying both came from an LLM.
Corrected above: that figure is from the toy-model probe. The broader design claim ("save the
parameter, not the context") is not retracted. It is bounded: confirmed for one narrow fact,
refuted at this budget for a procedure, and silent for the execution-skill class.

Sources: M-2234, M-2205, M-2206, M-2204
First seen: 2026-06-17
