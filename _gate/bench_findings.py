"""Bench findings renderer/checker (OPEN-0372 paper lane).

Reads read-only run ledgers (*.json) and cost logs (*.log) and renders a
per-run markdown table plus per-(arc, model) arm verdicts. Stdlib only.

Commands:
  render --ledgers DIR --logs DIR
  check  --ledgers DIR --logs DIR --doc FILE...
  write  --ledgers DIR --logs DIR --doc FILE...

`check` verifies that every `<!-- bench:run <run_id> --> ... <!-- bench:end -->`
block and every `<!-- bench:verdict <arc> <model> -->` line in the docs matches
what render would print; `write` regenerates them in place.
"""
import argparse
import glob
import json
import os
import re
import sys

# ---------------------------------------------------------------- log parsing

# A matched log line carries a literal `cost_usd=` whose value runs until the
# ` status=` field. `cost_usd_priced=` lines do NOT match (the char after
# `cost_usd` is `_`, not `=`), so they are ignored entirely.
_LOG_RE = re.compile(
    r"\[cost\]\s+(\S+)\s+"
    r"arm=(\S+)\s+"
    r"model=(\S+)\s+"
    r"turns=(\d+)\s+"
    r"tok_in=(\d+)\s+"
    r"tok_out=(\d+)\s+"
    r"cost_usd=(.*?)\s+"
    r"status=(\S+)"
)


def parse_cost(raw):
    """Clean float -> number; anything messy (unpriced(...), '0.0082 over ...') -> None."""
    if raw is None:
        return None
    try:
        return float(raw.strip())
    except (TypeError, ValueError):
        return None


def load_logs(logs_dir):
    """Return {(task_id, arm, model, tok_in): {'cost': float|None, 'status': str}}.

    First matching line per key wins.
    """
    index = {}
    for path in sorted(glob.glob(os.path.join(logs_dir, "*.log"))):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError:
            continue
        for line in lines:
            m = _LOG_RE.search(line)
            if not m:
                continue
            task_id, arm, model, turns, tok_in, tok_out, cost_raw, status = m.groups()
            key = (task_id, arm, model, int(tok_in))
            if key in index:
                continue
            index[key] = {"cost": parse_cost(cost_raw), "status": status,
                          "turns": int(turns), "tok_out": int(tok_out)}
    return index


# ------------------------------------------------------------- ledger loading

def load_runs(ledgers_dir):
    runs = []
    for path in sorted(glob.glob(os.path.join(ledgers_dir, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        runs.append(data)
    return runs


def is_pre_fix(run):
    """PRE-FIX iff no row carries dispatch_status."""
    rows = run.get("rows", []) or []
    return not any("dispatch_status" in r for r in rows)


# --------------------------------------------------------------- row semantics

def resolve_row(row, log_index):
    """-> (status, source, cost, log_status).

    status = dispatch_status if present, else matched log status, else "unknown".
    source = "ledger" | "log" | "none".
    """
    if "dispatch_status" in row and row.get("dispatch_status") is not None:
        status, source = row.get("dispatch_status"), "ledger"
    else:
        source = "none"
        status = None
    key = (row.get("task_id"), None, None, row.get("tokens_in"))
    # arm/model filled by caller via the row's parent run; see resolve_run_rows.
    log = log_index.get(key)
    log_status = log["status"] if log else None
    cost = log["cost"] if log else None
    if source == "none":
        if log_status is not None:
            status, source = log_status, "log"
        else:
            status, source = "unknown", "none"
    return status, source, cost, log_status


def resolve_run_rows(run, log_index):
    """Resolve every row of a run against the log index (arm/model from the run)."""
    arm = run.get("arm")
    model = run.get("model")
    out = []
    for row in run.get("rows", []) or []:
        key = (row.get("task_id"), arm, model, row.get("tokens_in"))
        log = log_index.get(key)
        log_status = log["status"] if log else None
        cost = log["cost"] if log else None
        if "dispatch_status" in row and row.get("dispatch_status") is not None:
            status, source = row.get("dispatch_status"), "ledger"
        elif log_status is not None:
            status, source = log_status, "log"
        else:
            status, source = "unknown", "none"
        corrected = "pass" if (row.get("gate_verdict") == "pass"
                               and status == "completed") else "fail"
        out.append({
            "row": row,
            "status": status,
            "source": source,
            "cost": cost,
            "log_status": log_status,
            "corrected": corrected,
        })
    return out


# ------------------------------------------------------------------- rendering

def _fmt_traps(items):
    if not items:
        return ""
    return ", ".join(str(x) for x in items)


def run_block(run, log_index):
    """The heading + markdown table + totals row, exactly as render prints it."""
    resolved = resolve_run_rows(run, log_index)
    gate = "PRE-FIX gate" if is_pre_fix(run) else "post-fix gate"
    lines = []
    lines.append("### {} \u2014 arc {} \u00b7 arm {} \u00b7 model {} \u00b7 {}".format(
        run.get("run_id"), run.get("arc_id"), run.get("arm"), run.get("model"), gate))
    lines.append("| task | status (source) | turns | tokens in | tokens out | "
                 "cost USD | gate recorded | gate corrected | traps hit | traps avoided |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")

    sum_turns = sum_tin = sum_tout = 0
    cost_sum = 0.0
    n_pass = 0
    for item in resolved:
        row = item["row"]
        cost = item["cost"]
        cost_cell = "n/a" if cost is None else "{:.4f}".format(cost)
        if cost is not None:
            cost_sum += cost
        sum_turns += row.get("turn_count") or 0
        sum_tin += row.get("tokens_in") or 0
        sum_tout += row.get("tokens_out") or 0
        if item["corrected"] == "pass":
            n_pass += 1
        lines.append("| {} | {} ({}) | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            row.get("task_id"),
            item["status"], item["source"],
            row.get("turn_count"), row.get("tokens_in"), row.get("tokens_out"),
            cost_cell,
            row.get("gate_verdict"), item["corrected"],
            _fmt_traps(row.get("traps_hit")),
            _fmt_traps(row.get("traps_avoided")),
        ))
    n = len(resolved)
    priced = any(item["cost"] is not None for item in resolved)
    lines.append("| **totals** |  | {} | {} | {} | {} |  | corrected {}/{} |  |  |".format(
        sum_turns, sum_tin, sum_tout, "{:.4f}".format(cost_sum) if priced else "n/a", n_pass, n))
    treat = treatment_line(run)
    if treat:
        lines.append("")
        lines.append(treat)
    return "\n".join(lines)


# arc_id -> {trap_id: banked atom slug}; filled from --manifests (each <dir>/<arc>/manifest.json).
TRAP_ATOMS = {}


def load_manifests(manifests_dir):
    for path in glob.glob(os.path.join(manifests_dir, "*", "manifest.json")):
        with open(path, encoding="utf-8") as fh:
            m = json.load(fh)
        TRAP_ATOMS[m.get("arc_id") or os.path.basename(os.path.dirname(path))] = {
            t.get("id"): t.get("atom_slug") for t in m.get("traps", []) if t.get("atom_slug")}


def treatment_line(run):
    """Manipulation check for a push arm: of the atoms banked for each task's own traps, how many
    reached the pushed working set. None when the run pushed nothing or no manifest is loaded."""
    if run.get("arm") == "A":
        rows = run.get("rows", [])
        n_q = sum(len((r.get("context_source") or {}).get("recall_queries") or []) for r in rows)
        n_t = sum(1 for r in rows if (r.get("context_source") or {}).get("recall_queries"))
        return ("Treatment delivered: {} pull-recall queries issued; {}/{} tasks queried the "
                "bank at all.".format(n_q, n_t, len(rows)))
    slugs = TRAP_ATOMS.get(run.get("arc_id"))
    rows = [r for r in run.get("rows", []) if (r.get("context_source") or {}).get("working_set")]
    if not slugs or not rows:
        return None
    want = got = 0
    for r in rows:
        ws = {str(w).replace("_", "-") for w in r["context_source"]["working_set"]}
        for trap in (r.get("traps_hit") or []) + (r.get("traps_avoided") or []):
            if trap in slugs:
                want += 1
                got += slugs[trap] in ws
    return ("Treatment delivered: {}/{} of the tasks' own banked trap atoms were in the pushed "
            "working set.".format(got, want))


def sorted_runs(runs):
    return sorted(runs, key=lambda r: (
        r.get("arc_id") or "", r.get("model") or "", r.get("arm") or "",
        r.get("ended_at") or ""))


# --------------------------------------------------------------------- verdict

def choose_run(runs):
    """Chosen run for one (arc, model, arm): latest ended_at among post-fix runs;
    fall back to the latest pre-fix run only when no post-fix run exists."""
    post = [r for r in runs if not is_pre_fix(r)]
    pool = post if post else runs
    if not pool:
        return None
    return max(pool, key=lambda r: r.get("ended_at") or "")


def corrected_counts(run, log_index):
    resolved = resolve_run_rows(run, log_index)
    n = len(resolved)
    p = sum(1 for it in resolved if it["corrected"] == "pass")
    return p, n


def verdict_for(arc, model, runs, log_index):
    """-> (verdict_text, run_id_A, run_id_B)."""
    same = [r for r in runs
            if (r.get("arc_id"), r.get("model")) == (arc, model)]
    a = choose_run([r for r in same if r.get("arm") == "A"])
    b = choose_run([r for r in same if r.get("arm") == "B"])
    a_id = a.get("run_id") if a else None
    b_id = b.get("run_id") if b else None
    if a is None and b is None:
        return "INCOMPLETE (no arms run)", a_id, b_id
    if a is None:
        return "INCOMPLETE (arm A not run)", a_id, b_id
    if b is None:
        return "INCOMPLETE (arm B not run)", a_id, b_id
    pa, na = corrected_counts(a, log_index)
    pb, nb = corrected_counts(b, log_index)
    if pa == na and pb == nb:
        verdict = "NULL (both arms clear)"
    elif pa == 0 and pb == 0:
        verdict = "NULL (both arms fail)"
    elif pa == pb:
        verdict = "NULL (equal pass count)"
    else:
        verdict = "SEPARATION A {}/{} vs B {}/{}".format(pa, na, pb, nb)
    return verdict, a_id, b_id


def all_arc_models(runs):
    keys = {(r.get("arc_id"), r.get("model")) for r in runs}
    return sorted(keys, key=lambda k: (k[0] or "", k[1] or ""))


def render(runs, log_index):
    chunks = []
    for run in sorted_runs(runs):
        chunks.append(run_block(run, log_index))
    verdict_lines = []
    for arc, model in all_arc_models(runs):
        verdict, a_id, b_id = verdict_for(arc, model, runs, log_index)
        verdict_lines.append("VERDICT {} {}: {} (A={}, B={})".format(
            arc, model, verdict, a_id, b_id))
    out = "\n\n".join(chunks)
    if verdict_lines:
        out = out + "\n\n" + "\n".join(verdict_lines)
    return out


# ------------------------------------------------------------------- doc I/O

_RUN_BLOCK_RE = re.compile(
    r"(<!--\s*bench:run\s+(\S+)\s*-->)(.*?)(<!--\s*bench:end\s*-->)", re.DOTALL)
_VERDICT_RE = re.compile(
    r"(<!--\s*bench:verdict\s+(\S+)\s+(\S+)\s*-->)(\r?\n)([^\r\n]*)")


def _norm_lines(s):
    lines = [ln.rstrip() for ln in s.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def _detect_nl(text):
    return "\r\n" if "\r\n" in text else "\n"


def check_doc(path, runs_by_id, log_index, runs):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()
    errors = []
    for m in _RUN_BLOCK_RE.finditer(text):
        run_id = m.group(2)
        run = runs_by_id.get(run_id)
        if run is None:
            errors.append("{}: unknown run_id {}".format(path, run_id))
            continue
        expected = run_block(run, log_index)
        if _norm_lines(m.group(3)) != _norm_lines(expected):
            errors.append(
                "{}: run {} block mismatch\n--- expected ---\n{}\n--- got ---\n{}".format(
                    path, run_id, expected, m.group(3).strip()))
    for m in _VERDICT_RE.finditer(text):
        arc, model = m.group(2), m.group(3)
        verdict, _a, _b = verdict_for(arc, model, runs, log_index)
        expected = "**Verdict: {}**".format(verdict)
        if m.group(5).rstrip() != expected:
            errors.append(
                "{}: verdict {}/{} mismatch\n--- expected ---\n{}\n--- got ---\n{}".format(
                    path, arc, model, expected, m.group(5)))
    return errors


def write_doc(path, runs_by_id, log_index, runs):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()
    nl = _detect_nl(text)

    def sub_run(m):
        run_id = m.group(2)
        run = runs_by_id.get(run_id)
        if run is None:
            return m.group(0)
        block = run_block(run, log_index).replace("\n", nl)
        return "{}{}{}{}<!-- bench:end -->".format(m.group(1), nl, block, nl)

    def sub_verdict(m):
        arc, model = m.group(2), m.group(3)
        verdict, _a, _b = verdict_for(arc, model, runs, log_index)
        return "{}{}**Verdict: {}**".format(m.group(1), nl, verdict)

    text = _RUN_BLOCK_RE.sub(sub_run, text)
    text = _VERDICT_RE.sub(sub_verdict, text)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# ----------------------------------------------------------------------- CLI

def _load(ledgers, logs):
    log_index = load_logs(logs)
    runs = load_runs(ledgers)
    runs_by_id = {}
    for r in runs:
        rid = r.get("run_id")
        if rid is not None:
            runs_by_id[rid] = r
    return runs, log_index, runs_by_id


def main(argv=None):
    parser = argparse.ArgumentParser(prog="bench_findings.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("--ledgers", required=True)
        p.add_argument("--logs", required=True)
        p.add_argument("--manifests", default=None, help="arcs dir; enables the treatment line")

    p_render = sub.add_parser("render")
    add_common(p_render)

    p_check = sub.add_parser("check")
    add_common(p_check)
    p_check.add_argument("--doc", nargs="+", required=True)

    p_write = sub.add_parser("write")
    add_common(p_write)
    p_write.add_argument("--doc", nargs="+", required=True)

    args = parser.parse_args(argv)
    if args.manifests:
        load_manifests(args.manifests)
    runs, log_index, runs_by_id = _load(args.ledgers, args.logs)

    if args.cmd == "render":
        sys.stdout.write(render(runs, log_index) + "\n")
        return 0

    if args.cmd == "check":
        errors = []
        for doc in args.doc:
            errors.extend(check_doc(doc, runs_by_id, log_index, runs))
        if errors:
            sys.stderr.write("\n".join(errors) + "\n")
            return 1
        return 0

    if args.cmd == "write":
        for doc in args.doc:
            write_doc(doc, runs_by_id, log_index, runs)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
