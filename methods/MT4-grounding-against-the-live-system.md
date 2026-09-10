# Documentation written from uploaded reference files, without querying the running system, invents mechanisms that already exist and fabricates ones that don't

**Claim.** When a language model authors a technical specification about a live system using only
uploaded reference documents as ground truth, it will produce confident, internally coherent, and
factually wrong output: inventing a parallel version of a mechanism that already exists under a
different name, fabricating the name of a component that was never built, and describing
configuration that no longer matches what is actually running. Each successive check against the
live system — first the memory bank, then the running command-line interface itself — finds and
corrects defects the previous, cheaper check could not see, and each pass costs less than the one
before it while catching more.

**Where it came from.** The setting is a memory-and-reasoning substrate an operator directs a
model to extend, on 2026-08-15. The model was asked to design a contract system that enforces a
build pipeline never skipping a phase. It first wrote roughly 80KB of specification from six
uploaded reference documents, without once querying the live system. That draft was then checked
in three successively cheaper passes: a semantic search of the memory bank, then reading full
records returned by that search, then running the actual command-line tool the system exposes.

**Evidence.** The first correction came from a single bank query that returned a "lukewarm" match
score of 0.383 (on a scale where "warm," meaning a proven path exists, starts at 0.45) against the
design intent — the system's own guidance for that band was "check the warmest result, you may be
near a known path." Acting on it surfaced that the draft had invented a six-tier model taxonomy
sitting beside a four-tier ladder already implemented and live, and had hardcoded specific model
vendor names where the live system deliberately abstracts that away because vendor bindings
rotate. The second pass, reading full records instead of search snippets, found the draft's
two-state "hot or cold" memory-match model was wrong: the live configuration defines three bands,
and the middle one ("lukewarm") has its own distinct behavior the two-state model could not
express.

The third pass queried the running command-line tool directly and found two defects neither
earlier pass could see. A provider connectivity check showed every configured model provider
reporting no API key — a state the uploaded docs could not reflect, since it depends on live
credentials, not anything written down. And the tool's own capability registry command found 26
registered capabilities, none named `frontend-build` — a name that appeared twice in the model's
own uploaded reference documentation, including a claim that a related capability "merged into"
it. The registry showed the underlying work existed under a different, already-registered name.
Across the full six-pass sequence, scope fell from a full custom workflow engine design down to
binding against two existing components. Cost of the ungrounded first draft, by the model's own
accounting: "most of a session."

**Mechanism.** The grounding sequence is not one check but three, cheapest-informative to
most-expensive-authoritative, each a distinct engine verb: `recall --warm "<intent>"` against the
bank (a semantic match returning warm/lukewarm/cold, roughly free), `remember <slug>` to read the
full body of whatever candidate the recall surfaced (a small weight cost on the atom used), and a
direct call to the system's own live command-line verbs (`providers --test`, `cartridge
registry`), which report state as of the current process, not as of whenever a document was last
edited. The rule encoded afterward as a standing check: before authoring more than roughly 200
lines of specification about the live system in a session, at least one `recall` call must have
happened; authoring past that line with zero recall calls fires a warning naming the cost of the
pattern it guards against. In five lines of pseudocode: (1) before writing a spec, call `recall
--warm` on the design intent; (2) if warm, treat the returned atom as ground truth over training;
(3) if lukewarm, `remember` the warmest candidate and check whether it already covers the design;
(4) regardless of bank result, call the system's live verbs for anything the spec asserts about
configuration, names, or credentials; (5) if a name or mechanism in the draft cannot be found
live, delete it rather than keep it on a reference document's word.

**What it could still be wrong about.** All three passes happened in one operator's session against
one system instance; "each pass is cheaper than the last" is observed once, not measured across
many draft-then-ground cycles, and could be specific to how errors cluster in one document rather
than a general property. The mechanism also assumes the live system is reachable and fast enough
to query mid-authoring; a slow or unreliable live check would change that tradeoff.

**Retractions / corrections.** The draft's own closing framing was corrected at the end of the
investigation: the model had proposed finishing a full specification for the one remaining
unbuilt piece before building anything. The operator rejected that with a direct counter-example —
a first-version compiler is never a good compiler, and its rules accrete from real bugs rather than
being specified complete in advance. The design shipped a minimal version instead, with one
enforcement rule drawn from the cost measured that session, and let further rules accrete only
when a real run exposed a real gap.

Sources: M-2525, M-2771, M-2712, M-2587, M-2769, M-1980
First seen: 2026-08-15
