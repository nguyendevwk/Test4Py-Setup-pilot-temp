import pytest
from thefuck.rules.git_rm_recursive import get_new_command


class DummyCommand:
    def __init__(self, parts):
        self.script_parts = parts


def test_get_new_command_inserts_r_flag():
    cmd = DummyCommand(['git', 'rm', 'file.txt'])
    new_cmd = get_new_command(cmd)
    assert new_cmd == 'git rm -r file.txt'


def test_get_new_command_handles_multiple_parts():
    cmd = DummyCommand(['git', 'rm', '-f', 'dir'])
    new_cmd = get_new_command(cmd)
    assert new_cmd == 'git rm -r -f dir'


def test_get_new_command_raises_value_error_when_rm_missing():
    cmd = DummyCommand(['git', 'add', 'file.txt'])
    with pytest.raises(ValueError):
        get_new_command(cmd)
