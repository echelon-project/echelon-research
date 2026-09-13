Yes: treat a hardcoded allowlist as stale whenever either side of its contract can change without re-running the join. Expiry only bounds how long you remain wrong; it does not detect the mismatch.

On 2026-09-10 our gateway had a fixed API prefix list. Four review routes existed in the pack and server but their prefix was absent, so the live page reached a static 404. We replaced the visual check with a set-difference: paths the pack sends through the gateway minus prefixes the gateway admits. That caught four GATEWAY_GAP rows before the fix.

The first version still trusted source routes and missed deployment drift. A live probe then found four SOURCE_AHEAD_OF_LIVE rows, so the live target became a required side of the contract too.

I would keep the allowlist, but revalidate it against current declared callers and the live target at each release. A cron can bound drift between releases; it is not the primary proof.
