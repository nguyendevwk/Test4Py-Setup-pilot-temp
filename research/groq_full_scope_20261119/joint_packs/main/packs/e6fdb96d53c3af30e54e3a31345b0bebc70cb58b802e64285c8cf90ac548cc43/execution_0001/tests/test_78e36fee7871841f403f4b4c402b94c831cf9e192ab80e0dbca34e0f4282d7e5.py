import pytest
from httpie.core import main
from httpie.status import ExitStatus

def test_main_debug_returns_success(tmp_path):
    """Passing '--debug' alone should print debug info and exit with SUCCESS."""
    status = main(args=['prog', '--debug'])
    assert status == ExitStatus.SUCCESS

def test_main_bytes_args_are_decoded(tmp_path):
    """Bytes arguments should be decoded using stdin encoding and processed."""
    # Use a byte string that is valid UTF-8
    status = main(args=['prog', b'--debug'])
    assert status == ExitStatus.SUCCESS

def test_main_unknown_option_returns_error(tmp_path):
    """An unknown command‑line option should result in an ERROR exit status."""
    status = main(args=['prog', '--unknown'])
    assert status == ExitStatus.ERROR
