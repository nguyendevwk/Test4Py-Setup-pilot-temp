import builtins
import io
import sys
import pytest
from thefuck.logs import already_configured

class DummyConfig:
    def __init__(self, reload):
        self.reload = reload

def test_already_configured_prints_expected_message(tmp_path):
    # Capture stdout
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        already_configured(DummyConfig(reload="thefuck reload"))
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    # The output should contain the reload command and the word "fuck"
    assert "thefuck reload" in output
    assert "fuck" in output
    # It should end with a period
    assert output.strip().endswith(".")

def test_already_configured_with_empty_reload(tmp_path):
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        already_configured(DummyConfig(reload=""))
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    # Even with empty reload, the message should still be printed
    assert "fuck" in output
    # The reload placeholder should be empty in the output
    assert "reload" not in output or output.count("reload") == 0

def test_already_configured_missing_reload_attribute():
    with pytest.raises(AttributeError):
        already_configured(object())
