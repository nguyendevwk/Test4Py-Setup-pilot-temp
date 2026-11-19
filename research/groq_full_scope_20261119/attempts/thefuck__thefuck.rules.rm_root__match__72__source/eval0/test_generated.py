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
    """Command does not contain both 'rm' and '/' in script_parts, should not match."""
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


def test_match_no_preserve_root_in_output():
    """Command contains 'rm' and '/' but output does not contain '--no-preserve-root'."""
    cmd = Command(
        script="rm /",
        output="rm: cannot remove '/': Directory not empty",
        cwd="/",
        env={},
        stdin="",
        stdout="",
        stderr="",
    )
    assert match(cmd) is False
