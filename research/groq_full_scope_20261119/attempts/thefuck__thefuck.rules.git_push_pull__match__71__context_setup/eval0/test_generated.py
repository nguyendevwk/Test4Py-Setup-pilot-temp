import pytest
from collections import namedtuple
from thefuck.rules.git_push_pull import match

Command = namedtuple('Command', ['script', 'output'])

def test_match_successful_rejection():
    """Command with a push that is rejected because the remote contains work."""
    script = "git push origin master"
    output = (
        "! [rejected]        master -> master (non-fast-forward)\n"
        "error: failed to push some refs to 'origin'\n"
        "Updates were rejected because the remote contains work that you do not have locally."
    )
    cmd = Command(script=script, output=output)
    assert match(cmd) is True

def test_match_no_push_in_script():
    """Command that does not contain 'push' should not match."""
    script = "git pull origin master"
    output = (
        "! [rejected]        master -> master (non-fast-forward)\n"
        "error: failed to push some refs to 'origin'\n"
        "Updates were rejected because the tip of your current branch is behind."
    )
    cmd = Command(script=script, output=output)
    assert match(cmd) is False

def test_match_incomplete_output():
    """Command with incomplete output should not match."""
    script = "git push origin master"
    output = (
        "! [rejected]        master -> master (non-fast-forward)\n"
        "error: failed to push some refs to 'origin'\n"
        # Missing the specific rejection reason
    )
    cmd = Command(script=script, output=output)
    assert match(cmd) is False
