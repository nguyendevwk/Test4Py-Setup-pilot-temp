import sys
import pytest
from httpie.core import main
from httpie.status import ExitStatus

def test_help_option_returns_ok(tmp_path):
    """Calling main with '-h' should return ExitStatus.OK and not raise."""
    status = main(args=['-h'])
    assert status == ExitStatus.OK

def test_invalid_url_returns_nonzero(tmp_path):
    """Providing an invalid URL should result in a non‑zero exit status."""
    status = main(args=['http://invalid_url'])
    assert status != ExitStatus.OK

def test_version_option_returns_ok(tmp_path):
    """The '--version' flag should return ExitStatus.OK."""
    status = main(args=['--version'])
    assert status == ExitStatus.OK
