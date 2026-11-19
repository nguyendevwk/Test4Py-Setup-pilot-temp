import io
import pytest
from httpie.core import print_debug_info
from httpie.plugins.registry import plugin_manager

class DummyEnv:
    """Simple environment stub with a writable stderr."""
    def __init__(self):
        self.stderr = io.StringIO()

def test_print_debug_info_outputs_expected_sections(tmp_path):
    """Verify that print_debug_info writes all expected sections to stderr."""
    env = DummyEnv()
    print_debug_info(env)
    output = env.stderr.getvalue()

    # Basic version lines
    assert f"HTTPie" in output
    assert f"Requests" in output
    assert f"Pygments" in output

    # Python version and executable
    assert "Python" in output
    assert str(sys.executable) in output

    # Platform info
    assert platform.system() in output

    # Environment representation
    assert repr(env) in output

    # Plugin manager representation
    assert repr(plugin_manager) in output

    # Ensure separators are present
    assert "\n\n" in output

def test_print_debug_info_handles_empty_stderr(tmp_path):
    """Ensure function works even if stderr is an empty StringIO."""
    env = DummyEnv()
    env.stderr = io.StringIO()  # explicitly empty
    print_debug_info(env)
    output = env.stderr.getvalue()
    # Should still contain the expected sections
    assert "HTTPie" in output
    assert "Requests" in output
    assert "Pygments" in output

def test_print_debug_info_raises_on_missing_stderr(tmp_path):
    """Passing an object without a stderr attribute should raise AttributeError."""
    class NoStderr:
        pass

    env = NoStderr()
    with pytest.raises(AttributeError):
        print_debug_info(env)
