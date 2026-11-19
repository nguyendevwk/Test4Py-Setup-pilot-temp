import io
import sys
import platform
import pytest
from httpie.core import print_debug_info
from httpie.plugins.registry import plugin_manager

class DummyEnv:
    def __init__(self):
        self.stderr = io.StringIO()

def test_print_debug_info_contains_expected_sections():
    env = DummyEnv()
    print_debug_info(env)
    output = env.stderr.getvalue()
    # Check that each component is present
    assert f"HTTPie {httpie.__version__}" in output
    assert f"Requests {requests.__version__}" in output
    assert f"Pygments {pygments.__version__}" in output
    assert f"Python {sys.version}" in output
    assert sys.executable in output
    assert f"{platform.system()} {platform.release()}" in output
    # Environment repr should be present
    assert repr(env) in output
    # Plugin manager repr should be present
    assert repr(plugin_manager) in output

def test_print_debug_info_with_minimal_env():
    class MinimalEnv:
        def __init__(self):
            self.stderr = io.StringIO()
    env = MinimalEnv()
    print_debug_info(env)
    output = env.stderr.getvalue()
    # Ensure no AttributeError and output is not empty
    assert output, "Output should not be empty"
    # Ensure that the output contains at least one newline
    assert "\n" in output

def test_print_debug_info_raises_on_missing_stderr():
    class BadEnv:
        pass
    env = BadEnv()
    with pytest.raises(AttributeError):
        print_debug_info(env)
