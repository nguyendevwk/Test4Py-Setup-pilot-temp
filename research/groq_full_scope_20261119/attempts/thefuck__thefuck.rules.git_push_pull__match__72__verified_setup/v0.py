import pytest
from thefuck.rules.git_push_pull import match

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_match_successful_push_rejection():
    script = "git push origin master"
    output = (
        "! [rejected]        master -> master (non-fast-forward)\n"
        "error: failed to push some refs to 'origin'\n"
        "Updates were rejected because the tip of your current branch is behind\n"
        "remote contains work that you do"
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is True

def test_match_missing_push_condition():
    script = "git pull origin master"
    output = (
        "! [rejected]        master -> master (non-fast-forward)\n"
        "error: failed to push some refs to 'origin'\n"
        "Updates were rejected because the tip of your current branch is behind\n"
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is False

def test_match_missing_attributes_raises():
    class IncompleteCommand:
        pass
    cmd = IncompleteCommand()
    with pytest.raises(AttributeError):
        match(cmd)
