import sys
import pytest
from thefuck.logs import version


def test_version_normal_output(capsys):
    """Verify that the normal call writes the expected string to stderr."""
    version("1.0.0", "3.11", "bash")
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "The Fuck 1.0.0 using Python 3.11 and bash\n"


def test_version_long_strings(capsys):
    """Verify that very long inputs are handled correctly."""
    long_ver = "v" * 1000
    long_py = "py" * 500
    long_shell = "sh" * 300
    version(long_ver, long_py, long_shell)
    out, err = capsys.readouterr()
    assert err == f"The Fuck {long_ver} using Python {long_py} and {long_shell}\n"


def test_version_non_string_inputs(capsys):
    """Verify that non‑string inputs are converted to strings without error."""
    version(42, 3.9, None)
    out, err = capsys.readouterr()
    assert err == "The Fuck 42 using Python 3.9 and None\n"
