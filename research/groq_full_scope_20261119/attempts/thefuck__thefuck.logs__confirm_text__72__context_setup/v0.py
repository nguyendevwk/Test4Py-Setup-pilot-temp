import sys
import io
import pytest
from thefuck.logs import confirm_text
from thefuck import const
from types import SimpleNamespace

# Helper to capture stderr output
@pytest.fixture
def captured_stderr():
    original_stderr = sys.stderr
    buf = io.StringIO()
    sys.stderr = buf
    yield buf
    sys.stderr = original_stderr

def test_confirm_text_no_side_effect_and_colors_enabled(captured_stderr, monkeypatch):
    # Ensure colors are enabled
    monkeypatch.setattr('thefuck.logs.settings.no_colors', False)
    cmd = SimpleNamespace(script='echo hello', side_effect=False)
    confirm_text(cmd)
    output = captured_stderr.getvalue()
    # Check that the command script appears
    assert 'echo hello' in output
    # Check that side effect marker is absent
    assert '(+side effect)' not in output
    # Check that color codes are present
    assert '\x1b[' in output  # ANSI escape sequences

def test_confirm_text_with_side_effect_and_colors_disabled(captured_stderr, monkeypatch):
    # Disable colors
    monkeypatch.setattr('thefuck.logs.settings.no_colors', True)
    cmd = SimpleNamespace(script='ls -l', side_effect=True)
    confirm_text(cmd)
    output = captured_stderr.getvalue()
    # Command script should be present
    assert 'ls -l' in output
    # Side effect marker should be present
    assert '(+side effect)' in output
    # No ANSI color codes should be present
    assert '\x1b[' not in output

def test_confirm_text_with_missing_attributes_raises_attribute_error(captured_stderr):
    # Pass an object lacking required attributes
    incomplete_cmd = SimpleNamespace()
    with pytest.raises(AttributeError):
        confirm_text(incomplete_cmd)
