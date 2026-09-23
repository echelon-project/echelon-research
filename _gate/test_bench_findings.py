"""Tests for _gate/bench_findings.py (synthetic fixtures only — never the real dirs)."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bench_findings as bf  # noqa: E402


# ------------------------------------------------------------------- helpers

def _row(task_id, gate="pass", turns=1, tin=100, tout=10,
         traps_hit=None, traps_avoided=None, dispatch=None, with_dispatch=True):
    r = {
        "task_id": task_id,
        "gate_verdict": gate,
        "turn_count": turns,
        "tokens_in": tin,
        "tokens_out": tout,
        "traps_hit": traps_hit or [],
        "traps_avoided": traps_avoided or [],
        "claims_vs_disk_divergences": 0,
        "context_source": {"kind": "recall", "recall_queries": []},
    }
    if with_dispatch:
        r["dispatch_status"] = dispatch
    return r


def _run(run_id, arc, arm, model, ended, rows):
    return {
        "arc_id": arc, "arm": arm, "model": model, "run_id": run_id,
        "dry_run": False, "started_at": ended, "ended_at": ended, "rows": rows,
    }


def _write_ledgers(dirpath, runs):
    for r in runs:
        with open(os.path.join(dirpath, r["run_id"] + ".json"), "w",
                  encoding="utf-8") as fh:
            json.dump(r, fh)


def _log_line(task, arm, model, turns, tin, tout, cost, status):
    return ("[cost] {} arm={} model={} turns={} tok_in={} tok_out={} "
            "cost_usd={} status={}").format(
        task, arm, model, turns, tin, tout, cost, status)


def _write_logs(dirpath, lines):
    with open(os.path.join(dirpath, "run.log"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- semantics

def test_pass_gate_but_timeout_is_corrected_fail():
    run = _run("R", "a", "A", "m", "2026-01-01T00:00:00+00:00",
               [_row("t01", gate="pass", dispatch="timeout")])
    resolved = bf.resolve_run_rows(run, {})
    assert resolved[0]["status"] == "timeout"
    assert resolved[0]["source"] == "ledger"
    assert resolved[0]["corrected"] == "fail"


def test_prefix_status_comes_from_matched_log():
    run = _run("R", "a", "A", "m", "2026-01-01T00:00:00+00:00",
               [_row("t01", gate="pass", with_dispatch=False)])
    log_index = bf.load_logs.__wrapped__ if False else ({})  # placeholder, real index built below
    # build a real index by parsing one line
    tmp = _parse_one(_log_line("t01", "A", "m", 1, 100, 10, "0.0286", "completed"))
    resolved = bf.resolve_run_rows(run, tmp)
    assert resolved[0]["status"] == "completed"
    assert resolved[0]["source"] == "log"
    assert resolved[0]["corrected"] == "pass"
    assert resolved[0]["cost"] == pytest.approx(0.0286)


def _parse_one(line):
    """Parse a single synthetic log line through the module's own regex."""
    m = bf._LOG_RE.search(line)
    task_id, arm, model, turns, tok_in, tok_out, cost_raw, status = m.groups()
    return {(task_id, arm, model, int(tok_in)):
            {"cost": bf.parse_cost(cost_raw), "status": status}}


def test_both_arms_all_pass_is_null_both_clear():
    runs = [
        _run("A1", "a", "A", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", dispatch="completed"),
              _row("t02", gate="pass", dispatch="completed")]),
        _run("B1", "a", "B", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", dispatch="completed"),
              _row("t02", gate="pass", dispatch="completed")]),
    ]
    verdict, a, b = bf.verdict_for("a", "m", runs, {})
    assert verdict == "NULL (both arms clear)"
    assert a == "A1" and b == "B1"


def test_both_arms_zero_is_null_both_fail():
    runs = [
        _run("A1", "a", "A", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", dispatch="timeout")]),
        _run("B1", "a", "B", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="fail", dispatch="partial")]),
    ]
    verdict, _a, _b = bf.verdict_for("a", "m", runs, {})
    assert verdict == "NULL (both arms fail)"


def test_separation_a1_of_3_vs_b0_of_3():
    runs = [
        _run("A1", "a", "A", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", dispatch="completed"),
              _row("t02", gate="pass", dispatch="timeout"),
              _row("t03", gate="pass", dispatch="timeout")]),
        _run("B1", "a", "B", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="fail", dispatch="partial"),
              _row("t02", gate="fail", dispatch="partial"),
              _row("t03", gate="fail", dispatch="partial")]),
    ]
    verdict, _a, _b = bf.verdict_for("a", "m", runs, {})
    assert verdict == "SEPARATION A 1/3 vs B 0/3"


def test_postfix_run_chosen_over_later_prefix_run():
    prefix = _run("PRE", "a", "A", "m", "2026-09-09T00:00:00+00:00",
                  [_row("t01", gate="pass", with_dispatch=False)])
    post = _run("POST", "a", "A", "m", "2026-01-01T00:00:00+00:00",
                [_row("t01", gate="pass", dispatch="completed")])
    chosen = bf.choose_run([prefix, post])
    assert chosen["run_id"] == "POST"


# ------------------------------------------------------------- cost parsing

def test_cost_parsing():
    assert bf.parse_cost("unpriced(model not in table)") is None
    assert bf.parse_cost("0.0082 over 12/23 calls; x") is None
    assert bf.parse_cost("0.0286") == pytest.approx(0.0286)


def test_render_cost_cells_unpriced_and_messy_are_na():
    runs = [
        _run("R", "a", "A", "m", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", with_dispatch=False, tin=100),
              _row("t02", gate="pass", with_dispatch=False, tin=200),
              _row("t03", gate="pass", with_dispatch=False, tin=300)]),
    ]
    logs = [
        _log_line("t01", "A", "m", 1, 100, 10, "unpriced(model not in table)", "completed"),
        _log_line("t02", "A", "m", 1, 200, 10, "0.0082 over 12/23 calls; x", "completed"),
        _log_line("t03", "A", "m", 1, 300, 10, "0.0286", "completed"),
    ]
    tmp = {}
    for ln in logs:
        tmp.update(_parse_one(ln))
    block = bf.run_block(runs[0], tmp)
    assert "| n/a |" in block          # unpriced row
    assert "0.0286" in block           # clean priced row
    assert "0.0082 over" not in block  # messy value never rendered raw


# ----------------------------------------------------------- check / write

def _mk_fixture(tmp_path):
    led = tmp_path / "runs"
    lg = tmp_path / "logs"
    led.mkdir()
    lg.mkdir()
    runs = [
        _run("A1", "arc1", "A", "model1", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", dispatch="completed"),
              _row("t02", gate="pass", dispatch="completed")]),
        _run("B1", "arc1", "B", "model1", "2026-01-01T00:00:00+00:00",
             [_row("t01", gate="pass", dispatch="completed"),
              _row("t02", gate="pass", dispatch="completed")]),
    ]
    _write_ledgers(str(led), runs)
    _write_logs(str(lg), [])
    return str(led), str(lg)


def _doc_path(tmp_path):
    doc = tmp_path / "F01.md"
    doc.write_text(
        "# Finding\n\n"
        "<!-- bench:run A1 -->\n"
        "stale content\n"
        "<!-- bench:end -->\n\n"
        "<!-- bench:verdict arc1 model1 -->\n"
        "stale verdict\n",
        encoding="utf-8")
    return str(doc)


def test_check_write_roundtrip(tmp_path):
    led, lg = _mk_fixture(tmp_path)
    doc = _doc_path(tmp_path)

    # before write, the stale doc must fail the check
    assert bf.main(["check", "--ledgers", led, "--logs", lg, "--doc", doc]) == 1

    # write regenerates, then check exits 0
    assert bf.main(["write", "--ledgers", led, "--logs", lg, "--doc", doc]) == 0
    assert bf.main(["check", "--ledgers", led, "--logs", lg, "--doc", doc]) == 0

    # hand-edit one table cell -> check must fail again
    text = open(doc, encoding="utf-8").read()
    assert "corrected 2/2" in text
    open(doc, "w", encoding="utf-8").write(text.replace("corrected 2/2", "corrected 9/9"))
    assert bf.main(["check", "--ledgers", led, "--logs", lg, "--doc", doc]) == 1


# ------------------------------------------------------- treatment + totals

def test_treatment_line_counts_only_the_tasks_own_trap_atoms(monkeypatch):
    monkeypatch.setattr(bf, "TRAP_ATOMS", {"a": {"trap-x": "atom-x", "trap-y": "atom-y"}})
    r1 = _row("t01", traps_avoided=["trap-x"])
    r1["context_source"] = {"kind": "governor", "working_set": ["atom_y", "other"]}
    r2 = _row("t02", traps_hit=["trap-y"])
    r2["context_source"] = {"kind": "governor", "working_set": ["atom_y"]}
    run = _run("R", "a", "B", "m", "2026-01-01T00:00:00+00:00", [r1, r2])
    # t01 needed atom-x (absent; atom-y is another task's lesson), t02 needed atom-y (present).
    assert bf.treatment_line(run) == ("Treatment delivered: 1/2 of the tasks' own banked trap "
                                      "atoms were in the pushed working set.")
    asked = _row("t02")
    asked["context_source"]["recall_queries"] = [{"query": "q"}, {"query": "q2"}]
    pull = _run("P", "a", "A", "m", "2026-01-01T00:00:00+00:00", [_row("t01"), asked])
    assert bf.treatment_line(pull) == ("Treatment delivered: 2 pull-recall queries issued; 1/2 "
                                       "tasks queried the bank at all.")


def test_totals_cost_is_na_when_no_row_is_priced():
    run = _run("R", "a", "A", "m", "2026-01-01T00:00:00+00:00", [_row("t01", dispatch="completed")])
    block = bf.run_block(run, {})
    totals = [ln for ln in block.splitlines() if ln.startswith("| **totals**")][0]
    assert totals.split("|")[6].strip() == "n/a"
