import pytest
from thefuck.rules.rm_root import match
from thefuck import Command


def test_match_successful_rm_root():
    """Command that removes root without preserve flag and output contains the flag."""
    cmd = Command(
        script="rm /",
        output="rm: cannot remove '/': Directory not empty\n--no-preserve-root",
        cwd="/",
        env={},
        stdin="",
        stdout="",
        stderr="",
    )
    assert match(cmd) is True


def test_match_no_rm_or_root():
    """Command does not contain both 'rm' and '/' in script_parts."""
    cmd = Command(
        script="rm -rf /tmp",
        output="--no-preserve-root",
        cwd="/",
        env={},
        stdin="",
        stdout="",
        stderr="",
    )
    # script_parts will be ['rm', '-rf', '/tmp']; '/' not present as separate part
    assert match(cmd) is False


def test_match_no_preserve_root_in_script():
    """Command includes '--no-preserve-root' in script, so it should not match."""
    cmd = Command(
        script="rm / --no-preserve-root",
        output="--no-preserve-root",
        cwd="/",
        env={},
        stdin="",
        stdout="",
        stderr="",
    )
    assert match(cmd) is False
