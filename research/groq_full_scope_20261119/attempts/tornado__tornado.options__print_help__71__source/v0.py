import io
import sys
import pytest
from tornado.options import define, options, clear_options
from tornado.options import print_help as tornado_print_help

# Ensure a clean state before each test
@pytest.fixture(autouse=True)
def reset_options():
    clear_options()
    yield
    clear_options()

def test_print_help_to_stderr(capsys):
    """print_help writes the help text to stderr by default."""
    # Define a sample option to have something in the help output
    define("sample", default=42, help="A sample integer option")
    # Call the target function
    tornado_print_help()
    # Capture stderr
    captured = capsys.readouterr()
    # The help text should contain the option name and its help string
    assert "sample" in captured.err
    assert "A sample integer option" in captured.err
    # The function returns None
    assert tornado_print_help() is None

def test_print_help_to_file(tmp_path):
    """print_help writes the help text to a provided file object."""
    define("flag", default=True, help="A boolean flag")
    file_path = tmp_path / "help.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        tornado_print_help(f)
    # Verify file contents
    content = file_path.read_text(encoding="utf-8")
    assert "flag" in content
    assert "A boolean flag" in content

def test_print_help_with_no_options_defined(capsys):
    """print_help works even when no options have been defined."""
    # Ensure no options are defined
    assert len(options) == 0
    tornado_print_help()
    captured = capsys.readouterr()
    # The help output should still contain the header
    assert "Options:" in captured.err
    # No specific option lines should appear
    assert "sample" not in captured.err
    assert "flag" not in captured.err
