# Every unit of work gets a package name and a declared interface before anyone writes code

**Claim.** A memory-and-agent system stops drowning in feature count when work is organized into
four layers with one job each — a door that holds no logic, a host that routes actions by reading
declarative wiring, packages that each own one task behind a versioned interface, and wiring files
that carry paths and settings instead of code — and a package counts as done only when its own
test suite passes against its declared interface, after which the rest of the system may talk to
it only through that interface.

**Where it came from.** The pattern is borrowed from a familiar shape: a Windows desktop
application built in C or C#, with an exe that owns the window and menus, a driver component that
reads installed packages and settings and routes clicks to the right one, plain configuration files
describing what is installed, and DLLs that each do one job behind a fixed interface. The owner of
an AI memory-and-agent estate had reached the point where adding the hundredth feature was
exhausting to reason about, because nothing was quarantined — every change could, in principle,
touch everything else. Naming the same four layers for the AI estate was ruled the default work
map for any project, in any language, not a Windows-specific trick.

**Evidence.** When the estate was measured against its own rule the same day, the gaps were
concrete: the command surface (a web board plus around 50 CLI verbs) still held logic that
belonged behind an interface; there was no real host, since different parts of the system reached
the core engine by sharing one Python environment instead of going through a router; the wiring
layer was mixed, with roughly sixty load-bearing files still defaulting to hard-coded local paths;
and the engine's own modules had no declared interfaces, no version numbers, and were tested file
by file rather than against a contract. Test material existed — reflex logs, run receipts, around
180 test files — but as raw material, not a scenario suite attached to any one package. This is a
self-audit, not an independent measurement, and no before/after comparison exists yet; the value is
the diagnostic, not a proven improvement.

**Mechanism.** Concretely, in five steps:

1. Before starting any unit of work, name the package it belongs to and the public interface
   (function names, argument order, return shape) it will expose or consume. A unit touching two
   packages splits into two units plus a wiring note.
2. Keep paths, ports, model names, and keys out of code. They live in a manifest (installed
   packages and versions), settings (user-owned), config (install-owned), and env (secrets) —
   never a hardcoded default that silently re-couples the code to one machine.
3. Build the package's scenario suite alongside the package: the dataset or test cases it is
   built, tested, and improved against. The suite is the only gate — a package is DONE the moment
   it passes against its declared interface, not when it "feels finished."
4. Record the package's state as a row in a build tracker (spec, checklist, evidence, open items).
   The row is the durable record of what was promised and shipped; a later change to a frozen
   package reopens its row as a gate event, the same way reopening a closed ticket would.
5. Keep the door — whatever is touched first — free of logic. Any verb in the door that does real
   work is a defect: move it behind a package interface. Once a package's suite is green and its
   row is closed, every caller reaches it only through that interface — nobody has to hold the
   whole system in their head, only the one package they are working inside.

"Freezing" a package means giving it a version number, a public interface list, a contract test
that fails the moment a name is dropped or a signature changes, and a `frozen` tag in its manifest
entry — it does not mean compiling it to a binary. Compiling to a shippable artifact is a decision
made only when a release leaves the building for an external server; inside the working estate,
source stays source so debugging tools and code-graph tools can still see into it. A
compiled-and-frozen module is opaque to exactly the tools that would find its bugs, and it locks
the code to one operating system and runtime version — the wrong tool for what was being asked
for, which was a boundary, not protection.

**What it could still be wrong about.** The self-measurement above is a snapshot from the day the
rule was adopted, done by the same people applying it, so it reads as a diagnostic checklist, not
evidence that the four-layer split reduces defects or rework over time. "Untouched since baseline"
was used as one signal for which modules were candidates to freeze first, but recent-inactivity is
a weak proxy for finished-and-correct — a module can be untouched because nobody has needed it yet.
No controlled before/after comparison has been run against a version of the estate that skipped
this map.

**Retractions / corrections.** None specific to this claim; the instinct to freeze code into a
compiled binary for "better management" was corrected the same day, in favor of the
boundary-not-binary version above.

Sources: M-1789, M-1826, M-2085
First seen: 2026-09-09
