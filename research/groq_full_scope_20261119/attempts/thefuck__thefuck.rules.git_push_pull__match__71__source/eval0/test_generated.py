import pytest
from thefuck.rules.git_push_pull import match

class DummyCommand:
    def __init__(self, script: str, output: str):
        self.script = script
        self.output = output

def test_match_returns_true_when_conditions_met():
    script = "git push origin main"
    output = (
        "! [rejected]        main -> main (non-fast-forward)\n"
        "error: failed to push some refs to 'https://github.com/user/repo.git'\n"
        "Updates were rejected because the tip of your current branch is behind\n"
        "origin/main."
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is True

def test_match_returns_false_when_push_missing():
    script = "git pull origin main"
    output = (
        "! [rejected]        main -> main (non-fast-forward)\n"
        "error: failed to push some refs to 'https://github.com/user/repo.git'\n"
        "Updates were rejected because the tip of your current branch is behind\n"
        "origin/main."
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is False

def test_match_returns_false_when_rejection_missing():
    script = "git push origin main"
    output = (
        "Counting objects: 3, done.\n"
        "Writing objects: 100% (3/3), 1.23 KiB | 1.23 KiB/s, done.\n"
        "Total 3 (delta 0), reused 0 (delta 0)\n"
        "To https://github.com/user/repo.git\n"
        "   abc1234..def5678  main -> main"
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is False
