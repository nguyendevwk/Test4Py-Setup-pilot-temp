import io
import os
import pytest
from thefuck.shells.generic import Generic
from thefuck.logs import warn

class DummyGeneric(Generic):
    """Subclass to override history file handling for testing."""
    def __init__(self, history_lines):
        super().__init__()
        self._history_lines = history_lines

    def _get_history_file_name(self):
        return ''

    def _get_history_lines(self):
        for line in self._history_lines:
            yield line

def test_expand_aliases_replaces_only_first_occurrence():
    g = Generic()
    # monkeypatch get_aliases to return a mapping
    g.get_aliases = lambda: {'ls': 'list'}
    # command with multiple occurrences of the alias
    cmd = 'ls -l && ls -a'
    expanded = g._expand_aliases(cmd)
    # only the first 'ls' should be replaced
    assert expanded == 'list -l && ls -a'
    # command without alias should remain unchanged
    assert g._expand_aliases('echo hello') == 'echo hello'

def test_split_command_handles_escaped_spaces_and_unicode():
    g = Generic()
    # command with escaped space and unicode character
    cmd = r'echo "Hello\ World" \u2603'
    parts = g.split_command(cmd)
    # shlex should split into ['echo', 'Hello World', '☃']
    assert parts == ['echo', 'Hello World', '☃']
    # ensure that a simple command splits correctly
    assert g.split_command('ls -la') == ['ls', '-la']

def test_info_handles_exception_from_get_version(monkeypatch):
    g = Generic()
    # monkeypatch _get_version to raise an exception
    def raise_exc():
        raise RuntimeError('version not found')
    monkeypatch.setattr(g, '_get_version', raise_exc)
    # capture warn output
    messages = []
    def fake_warn(msg):
        messages.append(msg)
    monkeypatch.setattr(warn, '__call__', fake_warn)
    # call info and verify it returns only friendly_name
    result = g.info()
    assert result == 'Generic Shell'
    # verify that warn was called with the expected message
    assert any('Could not determine shell version' in m for m in messages)
