"""Unit tests for Council Architecture."""
import json
import pytest
from pathlib import Path
from council.critic import clean_code_block, audit_test_quality
from council.engine import CouncilEngine
from council.runner import run_council_pipeline

def test_clean_code_block():
    raw_markdown = """Here is the test case:
```python
import pytest

def test_example():
    assert 1 + 1 == 2
```
Hope this helps!"""
    cleaned = clean_code_block(raw_markdown)
    assert "assert 1 + 1 == 2" in cleaned
    assert "Hope this helps" not in cleaned


def test_clean_code_block_strips_think_tags():
    raw_reasoning = """<think>
Let's see: I need to write a test function.
First import pytest.
</think>
```python
def test_calc():
    assert 2 * 2 == 4
```"""
    cleaned = clean_code_block(raw_reasoning)
    assert "<think>" not in cleaned
    assert "test_calc" in cleaned


def test_audit_test_quality():
    good_code = """
def test_valid():
    assert True
"""
    audit = audit_test_quality(good_code)
    assert audit["valid_ast"] is True
    assert audit["test_functions"] == 1
    assert audit["assertion_count"] == 1
    assert audit["is_hollow"] is False

    hollow_code = """
def test_hollow():
    x = 10
"""
    audit_hollow = audit_test_quality(hollow_code)
    assert audit_hollow["is_hollow"] is True
    assert audit_hollow["assertion_count"] == 0


def test_council_engine_mock():
    engine = CouncilEngine(mock=True)
    res_coder = engine.call_coder("sys", "user")
    assert "test_mock" in res_coder
    assert engine.telemetry["coder_calls"] == 1

    res_critic = engine.call_critic("sys", "user")
    assert "test_mock_repaired" in res_critic
    assert engine.telemetry["critic_calls"] == 1


def test_council_pipeline_mock(tmp_path):
    class Args:
        samples = 1
        mode = "council"
        coder_model = "mock-coder"
        critic_model = "mock-critic"
        no_repair = False
        max_new_tokens = 512
        mock = True
        output = tmp_path / "council_test"

    summary = run_council_pipeline(Args())
    assert summary["samples"] == 1
    assert (Args.output / "report.md").exists()
    assert (Args.output / "summary.json").exists()
