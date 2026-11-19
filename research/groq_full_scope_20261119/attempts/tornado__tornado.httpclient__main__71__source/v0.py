import pytest
import sys
import types

# Import the target module
import tornado.httpclient as httpclient

def test_main_raises_system_exit_when_no_args():
    """
    The main function should raise SystemExit when invoked without command line arguments.
    This is the expected behavior of tornado.options.parse_command_line when no URLs are provided.
    """
    # Temporarily replace sys.argv to simulate running without arguments
    original_argv = sys.argv
    sys.argv = [original_argv[0]]
    try:
        with pytest.raises(SystemExit):
            httpclient.main()
    finally:
        sys.argv = original_argv

def test_main_is_callable_and_returns_none():
    """
    Verify that the main function is callable and its return type is None.
    The function is expected to perform side effects and not return a value.
    """
    assert callable(httpclient.main)
    # Since main may raise SystemExit, we catch it to inspect the return value
    original_argv = sys.argv
    sys.argv = [original_argv[0], "http://example.com"]
    try:
        with pytest.raises(SystemExit):
            result = httpclient.main()
        assert result is None
    finally:
        sys.argv = original_argv

def test_main_exists_in_module():
    """
    Ensure that the main function is present in the module's namespace.
    """
    assert hasattr(httpclient, "main")
    assert isinstance(httpclient.main, types.FunctionType)
