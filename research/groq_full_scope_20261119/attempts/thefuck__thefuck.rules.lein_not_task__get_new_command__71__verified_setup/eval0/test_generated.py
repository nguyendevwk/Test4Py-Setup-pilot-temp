import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, command, output):
        self.command = command
        self.output = output

def test_get_new_command_replaces_first_suggestion(tmp_path):
    # Simulate a command that failed with a missing task error
    output = (
        "lein test 'foo' is not a task\n"
        "Did you mean this?\n"
        "  lein test foo\n"
        "  lein test bar\n"
    )
    cmd = DummyCommand("lein test 'foo'", output)
    new_cmd = get_new_command(cmd)
    # The broken part "'foo'" should be replaced by the first suggestion "lein test foo"
    assert "lein test foo" in new_cmd
    assert "'foo'" not in new_cmd

def test_get_new_command_uses_only_first_suggestion(tmp_path):
    # Multiple suggestions; ensure only the first is used
    output = (
        "lein test 'baz' is not a task\n"
        "Did you mean this?\n"
        "  lein test baz\n"
        "  lein test qux\n"
    )
    cmd = DummyCommand("lein test 'baz'", output)
    new_cmd = get_new_command(cmd)
    # Should contain the first suggestion but not the second
    assert "lein test baz" in new_cmd
    assert "lein test qux" not in new_cmd

def test_get_new_command_raises_index_error_when_no_match(tmp_path):
    # Output without the expected pattern should raise IndexError
    output = (
        "lein test 'missing' is not a task\n"
        "Some unrelated error message\n"
    )
    cmd = DummyCommand("lein test 'missing'", output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
