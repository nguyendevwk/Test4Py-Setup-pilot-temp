import sys
import io
import pytest
from thefuck.logs import debug
from thefuck.conf import settings
from colorama import Style, Fore

# Helper to capture stderr
@pytest.fixture
def cap_stderr():
    original = sys.stderr
    buffer = io.StringIO()
    sys.stderr = buffer
    yield buffer
    sys.stderr = original

def test_debug_enabled_writes_formatted(cap_stderr):
    settings.debug = True
    debug("Test message")
    output = cap_stderr.getvalue()
    # Expected format: BLUE + BOLD + "DEBUG:" + RESET + " Test message\n"
    expected_prefix = f"{Fore.BLUE}{Style.BRIGHT}DEBUG:{Style.RESET_ALL} "
    assert output.startswith(expected_prefix)
    assert output.endswith("\n")
    assert "Test message" in output

def test_debug_disabled_does_not_write(cap_stderr):
    settings.debug = False
    debug("Should not appear")
    output = cap_stderr.getvalue()
    assert output == ""

def test_debug_with_special_characters(cap_stderr):
    settings.debug = True
    special_msg = "Line1\nLine2\tUnicode: \u2603"
    debug(special_msg)
    output = cap_stderr.getvalue()
    # Ensure the message is present verbatim after the prefix
    prefix = f"{Fore.BLUE}{Style.BRIGHT}DEBUG:{Style.RESET_ALL} "
    assert output.startswith(prefix)
    assert output.endswith("\n")
    # The message part should match exactly
    assert output[len(prefix):-1] == special_msg
