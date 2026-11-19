import io
import platform
import sys
import pytest
from httpie.core import print_debug_info
from httpie.context import Environment
from httpie.plugins.registry import plugin_manager

def test_print_debug_info_basic_output(tmp_path):
    """Verify that the debug info contains expected headers and environment details."""
    # Create a temporary file to capture stderr output
    stderr_file = tmp_path / "stderr.txt"
    with open(stderr_file, "w", encoding="utf-8") as f:
        env = Environment(args=[], config={})
        env.stderr = f
        print_debug_info(env)

    # Read the captured output
    output = stderr_file.read_text(encoding="utf-8")

    # Check that the output contains the expected headers
    assert f"HTTPie {env.__class__.__module__}" in output or "HTTPie" in output
    assert f"Requests {sys.modules['requests'].__version__}" in output or "Requests" in output
    assert f"Pygments {sys.modules['pygments'].__version__}" in output or "Pygments" in output
    assert f"Python {sys.version}" in output
    assert sys.executable in output
    assert f"{platform.system()} {platform.release()}" in output

    # Ensure the environment representation is present
    assert repr(env) in output

    # Ensure the plugin manager representation is present
    assert repr(plugin_manager) in output

def test_print_debug_info_stringio_output():
    """Verify that the function writes to a StringIO object correctly."""
    string_io = io.StringIO()
    env = Environment(args=[], config={})
    env.stderr = string_io
    print_debug_info(env)

    output = string_io.getvalue()

    # The output should start with the HTTPie header
    assert output.startswith("HTTPie")
    # It should contain the Requests header
    assert "Requests" in output
    # It should contain the Pygments header
    assert "Pygments" in output
    # It should contain the Python version
    assert f"Python {sys.version}" in output
    # It should contain the platform info
    assert f"{platform.system()} {platform.release()}" in output
    # It should contain the environment representation
    assert repr(env) in output
    # It should contain the plugin manager representation
    assert repr(plugin_manager) in output

def test_print_debug_info_with_custom_stderr(tmp_path):
    """Verify that the function works when stderr is a custom file-like object."""
    class CustomStderr(io.StringIO):
        def write(self, s):
            # Simulate a write that appends a marker
            super().write(s)
            super().write("[MARKER]")

    custom_stderr = CustomStderr()
    env = Environment(args=[], config={})
    env.stderr = custom_stderr
    print_debug_info(env)

    output = custom_stderr.getvalue()

    # Ensure that the marker appears after each write
    assert "[MARKER]" in output
    # Ensure that the output still contains the expected headers
    assert "HTTPie" in output
    assert "Requests" in output
    assert "Pygments" in output
    assert f"Python {sys.version}" in output
    assert f"{platform.system()} {platform.release()}" in output
    assert repr(env) in output
    assert repr(plugin_manager) in output
