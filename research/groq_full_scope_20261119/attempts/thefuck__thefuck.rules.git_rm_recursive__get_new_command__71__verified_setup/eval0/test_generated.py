import pytest
from thefuck.rules.git_rm_recursive import get_new_command


class DummyCommand:
    def __init__(self, script_parts):
        self.script_parts = script_parts


def test_get_new_command_inserts_recursively():
    cmd = DummyCommand(['git', 'rm', 'file.txt'])
    new_cmd = get_new_command(cmd)
    assert new_cmd == 'git rm -r file.txt'


def test_get_new_command_handles_multiple_parts():
    cmd = DummyCommand(['git', 'rm', '-f', 'file.txt'])
    new_cmd = get_new_command(cmd)
    assert new_cmd == 'git rm -r -f file.txt'


def test_get_new_command_raises_when_rm_missing():
    cmd = DummyCommand(['git', 'add', 'file.txt'])
    with pytest.raises(ValueError):
        get_new_command(cmd)
