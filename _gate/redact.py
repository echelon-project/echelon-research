"""Redaction gate: refuse any file in 02- that carries private material.
Usage: python redact.py <path-or-dir> [--fix-report out.json]
Exit 1 on any hit. Patterns are conservative; a hit is a human decision, not auto-scrub.
"""
import re, sys, json, pathlib
PATTERNS = {
  "credential": r"(?i)(api[_-]?key\s*[:=]|secret\s*[:=]|(access|auth|bearer|api)[ _-]?token\s*[:=]|password\s*[:=]|passwd|Bearer\s+[A-Za-z0-9._-]{16,}|sk-[A-Za-z0-9]{16,}|gho_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|LM_API_TOKEN|\.apikey)",
  "client-name": r"(?i)\b(moladin|ladeloux|kiki|hokiemas|jokibandar|nobarcantik|rnee|waroenk|kito|rumahbungsu|calbet|satu-?ai|bee-?edge|mazda|komdigi|willy soemantri|atsoftware)\b",
  "person": r"(?i)\b(goravine|gorav|kenny|heri|teng)\b",  # author's name is published by choice
  "customer-data": r"(?i)(\bRp\.?\s?\d|\bIDR\b|\bNIK\b|\bKTP\b|\bNPWP\b|@gmail\.com|\+62\d{8,}|\b08\d{8,}\b)",
  "host": r"(?i)(\b\d{1,3}(\.\d{1,3}){3}\b|\.ladeloux\.com|captain\.|caprover)",
}
ALLOW=("albertteng78@gmail.com",)
def scan(p):
  hits=[]
  try: txt=p.read_text(encoding="utf-8",errors="ignore")
  except Exception: return hits
  for i,line in enumerate(txt.splitlines(),1):
    for a in ALLOW: line=line.replace(a,"")
    for k,rx in PATTERNS.items():
      m=re.search(rx,line)
      if m: hits.append({"file":str(p),"line":i,"kind":k,"match":m.group(0)[:40]})
  return hits
root=pathlib.Path(sys.argv[1]); files=[root] if root.is_file() else [f for f in root.rglob("*") if f.suffix.lower() in {".md",".txt",".json",".rst"} and "_gate" not in f.parts and "_ledger" not in f.parts]
allhits=[h for f in files for h in scan(f)]
if "--fix-report" in sys.argv: json.dump(allhits,open(sys.argv[sys.argv.index("--fix-report")+1],"w"),indent=1)
for h in allhits[:200]: print(f'{h["kind"]:14} {h["file"]}:{h["line"]}  {h["match"]}')
print(f"REDACTION GATE: {len(allhits)} hit(s) in {len(files)} file(s) -> {'FAIL' if allhits else 'PASS'}")
sys.exit(1 if allhits else 0)
