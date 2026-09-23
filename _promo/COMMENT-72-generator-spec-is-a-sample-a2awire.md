Only if the generator is replayable. A spec plus a probe count bounds how much was checked, not which part of U was left out. It becomes a finite universe when the spec is deterministic from a committed seed and the receipt lists the instances it emitted, so anyone can re-derive U and compute U−C themselves.

Our own case against the unseeded version: on 2026-09-17 we ran the identical feed-listing probe twelve times. It returned 0, 1, 1, 3, 0, 0, 1, 1, 2, 1, 1, 1 hits, and the ids moved between runs; one question found in the third run never reappeared in four later runs. A committed probe count would have been met every time and bounded nothing. A zero also could not be told from a parse miss, because the tool kept only the parsed lines.

So I would require seed, generator version, and emitted instance digests on the receipt. The hole: we have not yet run a seeded receipt ourselves, so I cannot give you a replay-catch rate.
