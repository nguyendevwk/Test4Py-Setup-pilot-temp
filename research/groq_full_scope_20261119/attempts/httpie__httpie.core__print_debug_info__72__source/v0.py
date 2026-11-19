import io
import sys
import platform
import pytest
from httpie.core import print_debug_info
from httpie.context import Environment
from httpie.plugins.registry import plugin_manager

def test_print_debug_info_writes_expected_sections(tmp_path):
    """Verify that print_debug_info writes all expected sections to stderr."""
    # Create a temporary file to capture stderr output
    stderr_file = tmp_path / "stderr.txt"
    env = Environment(stderr=stderr_file.open("w"))
    try:
        print_debug_info(env)
    finally:
        stderr_file.close()

    content = stderr_file.read_text()
    # Check HTTPie, Requests, Pygments, Python, and platform info
    assert f"HTTPie {__import__('httpie').__version__}" in content
    assert f"Requests {__import__('requests').__version__}" in content
    assert f"Pygments {__import__('pygments').__version__}" in content
    assert f"Python {sys.version}" in content
    assert sys.executable in content
    assert f"{platform.system()} {platform.release()}" in content

    # Environment repr should be present
    assert repr(env) in content

    # Plugin manager repr should be present
    assert repr(plugin_manager) in content

def test_print_debug_info_with_stringio_stderr():
    """Ensure the function works when stderr is a StringIO object."""
    stderr_io = io.StringIO()
    env = Environment(stderr=stderr_io)
    print_debug_info(env)
    output = stderr_io.getvalue()
    # Basic sanity checks
    assert "HTTPie" in output
    assert "Requests" in output
    assert "Pygments" in output
    assert "Python" in output
    assert repr(env) in output
    assert repr(plugin_manager) in output

def test_print_debug_info_raises_on_missing_stderr():
    """Passing an Environment without a stderr attribute should raise AttributeError."""
    class DummyEnv:
        pass  # No stderr attribute

    dummy_env = DummyEnv()
    with pytest.raises(AttributeError):
        print_debug_info(dummy_env)
