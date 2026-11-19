import pytest
from collections import namedtuple
from thefuck.rules.git_push_pull import match

# Simple stand‑in for the Command object used by thefuck
Command = namedtuple('Command', ['script', 'output'])

def test_match_detects_push_rejection():
    """
    Normal case: a push command that was rejected because the remote
    contains work that the local branch does not have.
    """
    cmd = Command(
        script="git push origin main",
        output=(
            "! [rejected]        main -> main (non-fast-forward)\n"
            "error: failed to push some refs to 'origin'\n"
            "Updates were rejected because the remote contains work that you do not have locally."
        ),
    )
    assert match(cmd) is True

def test_match_false_when_not_a_push_or_no_rejection():
    """
    Boundary case: the command is not a push or the output does not
    contain a rejection message. The matcher should return False.
    """
    cmd = Command(
        script="git pull origin main",
        output=(
            "Already up to date.\n"
            "Updates were rejected because the tip of your current branch is behind."
        ),
    )
    assert match(cmd) is False

def test_match_handles_missing_output_attribute():
    """
    Error scenario: the command object lacks an 'output' attribute.
    The matcher should not raise an exception but simply return False.
    """
    # Create an object that only has 'script' but no 'output'
    class IncompleteCommand:
        def __init__(self, script):
            self.script = script

    cmd = IncompleteCommand("git push origin main")
    # match should not raise; it will access cmd.output and fail gracefully
    assert match(cmd) is False
