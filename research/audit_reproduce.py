"""Offline reviewer checks. Synthetic inputs verify reporting, not model efficacy.

Run from repository root: python3 -m research.audit_reproduce
No downloads, GPU, upstream checkout, or production edits.
"""
import contextlib
import io
import json
import sys
import tempfile
import types
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from council import runner
from council.critic import audit_test_quality
from council.engine import CouncilEngine
from ablation_runner import compile_ablation_reports


def main():
    observations = {}
    with tempfile.TemporaryDirectory(prefix="review-integrity-") as directory:
        root = Path(directory)

        def checkout(url, revision, dst):
            dst.mkdir(parents=True)

        # A mixed suite: one passing and one failing test.
        report = {"tests": [
            {"nodeid": "test_generated.py::test_ok", "outcome": "passed", "call": {"outcome": "passed"}},
            {"nodeid": "test_generated.py::test_bad", "outcome": "failed", "call": {"outcome": "failed"}},
        ]}
        scoring = {"status": "unstable_original", "passed": 1,
                   "branch_coverage": {"module": {"covered_branches": 0, "num_branches": 10}},
                   "mutation_score": None}
        args = SimpleNamespace(output=root / "mixed", samples=1, mode="baseline",
            coder_model="synthetic-coder", critic_model="synthetic-critic",
            mock=True, max_new_tokens=512, no_repair=False, load_in_4bit=False)
        with patch.dict(sys.modules, {"pytest_jsonreport": types.ModuleType("pytest_jsonreport")}), \
             patch.object(runner, "checkout", checkout), \
             patch.object(runner, "source_context", return_value="synthetic source"), \
             patch.object(runner, "generate_test_with_coder", return_value="def test_ok():\n    assert True\ndef test_bad():\n    assert False\n"), \
             patch.object(runner, "pytest_run", return_value=({"returncode": 1, "stdout": "1 failed, 1 passed", "stderr": ""}, report, root)), \
             patch.object(runner, "score", return_value=scoring), \
             patch.object(runner, "repair_with_critic") as repair, \
             contextlib.redirect_stdout(io.StringIO()):
            summary = runner.run_council_pipeline(args)
        row = summary["results"][0]
        assert row["status"] == "passed" and summary["passed_samples"] == 1
        assert row["branch_pct"] is None
        assert not repair.called
        assert "mock" not in summary
        observations["mixed_suite_and_unstable_score"] = row
        observations["critic_called_for_partial_failure"] = repair.called
        observations["zero_coverage_recorded_as"] = row["branch_pct"]
        observations["mock_flag_in_summary"] = "mock" in summary

        # A missing observation is omitted from the metric's denominator.
        folder = root / "aggregation" / "synthetic"
        folder.mkdir(parents=True)
        (folder / "summary.json").write_text(json.dumps({
            "samples": 2, "passed_samples": 1,
            "results": [{"branch_pct": 80, "mutation_score": 1},
                        {"branch_pct": None, "mutation_score": None}]}))
        with contextlib.redirect_stdout(io.StringIO()):
            table = compile_ablation_reports(folder.parent)
        assert "80.0% | 1.00" in table
        observations["conditional_means_without_metric_denominators"] = table

    mock_code = CouncilEngine(mock=True).call_coder("", "")
    observations["mock_output"] = mock_code
    observations["tautology_quality_audit"] = audit_test_quality("def test_empty_behavior():\n    assert True\n")
    assert observations["tautology_quality_audit"]["is_hollow"] is False
    print(json.dumps(observations, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
