import sys
import pytest
from httpie.core import main
from httpie.status import ExitStatus


def test_help_exit_success(capsys):
    """Calling main with --help should exit successfully and print usage."""
    # The first argument is the program name; subsequent args are parsed.
    exit_status = main(['httpie', '--help'])
    captured = capsys.readouterr()
    # The help text should contain the program name and a usage line.
    assert "Usage:" in captured.out
    assert exit_status == ExitStatus.SUCCESS


def test_version_output(capsys):
    """Calling main with --version should print the version and exit successfully."""
    exit_status = main(['httpie', '--version'])
    captured = capsys.readouterr()
    # The output should contain the httpie version string.
    assert "httpie" in captured.out.lower()
    assert exit_status == ExitStatus.SUCCESS


def test_invalid_option_raises_system_exit():
    """Providing an unknown option should raise SystemExit with code 2."""
    with pytest.raises(SystemExit) as excinfo:
        main(['httpie', '--unknown-option'])
    # SystemExit code 2 indicates a usage error.
    assert excinfo.value.code == 2
