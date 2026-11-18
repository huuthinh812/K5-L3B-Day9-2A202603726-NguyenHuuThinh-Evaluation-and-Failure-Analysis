"""Run public submission checks and record real output, including expected failures.

Run from src/: python -m lab9.verify
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> int:
    commands = [
        (["pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider"], 0),
        (["lab9.smoke"], 0),
        (["lab9.evalset", "--check"], 0),
        (["lab9.evalset", "--v2"], 0),
        (["lab9.judge", "--csv", "data/eval/judge_tone_public.csv", "--audit", "5"], 0),
        (["lab9.judge", "--csv", "data/eval/judge_helpful_public.csv", "--audit", "5"], 1),
        (["lab9.eval", "--shape", "swarm", "--out", "reports/eval_pr.json"], 0),
        (["lab9.ci_check", "--pr", "reports/eval_pr.json", "--baseline", "reports/baseline_v1.json", "--spec", "config/metric_spec.yaml"], 0),
        (["lab9.gate", "--pr", "reports/eval_pr.json", "--baseline", "reports/baseline_v1.json"], 0),
        (["lab9.gate", "--pr", "reports/eval_fixed.json", "--baseline", "reports/baseline_v1.json"], 0),
        (["lab9.gate", "--pr", "reports/eval_seeded_regression.json", "--baseline", "reports/baseline_v1.json"], 1),
        (["lab9.mutation", "--detect"], 0),
        (["lab9.gate", "--pr", "reports/baseline_v2.json", "--baseline", "reports/baseline_v2.json", "--spec", "config/metric_spec_v2.yaml"], 0),
        (["lab9.mutation", "--spec", "config/metric_spec_v2.yaml", "--baseline", "reports/baseline_v2.json"], 0),
        (["lab9.mutation", "--spec", "config/metric_spec_v2.yaml", "--aa", "66,77,88,99,110"], 0),
        (["lab9.traps", "--pr", "reports/eval_slice_regression.json", "--baseline", "reports/baseline_v2.json", "--spec", "config/metric_spec_v2.yaml"], 0),
    ]
    log = ["Public verification — Nguyễn Hữu Thịnh\n"]
    failures = []
    with tempfile.TemporaryDirectory(prefix="lab9-verify-") as tmp:
        env = {**os.environ, "PYTHONUTF8": "1", "TEMP": tmp, "TMP": tmp}
        for args, expected in commands:
            command = [sys.executable, "-m", *args]
            line = "python -m " + " ".join(args)
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env=env)
            output = "\n".join(line.rstrip() for line in (result.stdout + result.stderr).splitlines()) + "\n"
            ok = result.returncode == expected
            if args[0] == "lab9.gate" and expected == 1:
                ok &= "exit 1 — blocked:" in output and "pass_rate" in output.split("exit 1 — blocked:")[-1]
            if "--aa" in args:
                deltas = [float(row.split()[-1]) for row in result.stdout.splitlines()[1:] if row.strip()]
                ok &= bool(deltas) and all(delta == 0 for delta in deltas)
            if not ok:
                failures.append(line)
            section = f"\n$ {line}\n{output}\nexit={result.returncode}, expected={expected}: {'PASS' if ok else 'FAIL'}\n"
            print(section, flush=True)
            log.append(section)
    summary = f"\n{len(commands) - len(failures)}/{len(commands)} checks passed\n"
    log.append(summary)
    Path("reports").mkdir(exist_ok=True)
    Path("reports/validation_m6_m7.txt").write_text("".join(log), encoding="utf-8")
    print(summary)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
