# claims.jsonl row

{
  "id": "C-0001",
  "claim": "one sentence, falsifiable",
  "kind": "finding | technique | method | hypothesis | law | retraction",
  "first_seen": "YYYY-MM-DD",
  "source": "01-relative path of the doc it was mined from",
  "evidence": "quoted line(s) or measured number, with where it was measured",
  "status": "witnessed | hypothesis | retracted | superseded",
  "supersedes": "C-xxxx or null",
  "topic": "memory | recall | reflex | gate | tiering | harness | boundary | identity | economics | other",
  "redaction_flags": ["client-name", "person", "credential", "customer-data"]   // empty if clean
}

witnessed  = an atom/receipt/ruling records it being used and paying off, or a number was measured
hypothesis = stated, never measured
retracted  = the record itself withdrew it (keep; retractions are evidence of method)
superseded = replaced by a later claim (link it)
