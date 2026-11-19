import sys
import types
import pytest
from thefuck.logs import show_corrected_command, color
from thefuck import const

# Dummy corrected command object
class DummyCommand:
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect

def test_show_corrected_command_with_side_effect(capsys, monkeypatch):
    # Ensure colors are enabled
    monkeypatch.setattr('thefuck.conf.settings.no_colors', False)
    cmd = DummyCommand('ls -la', side_effect=True)
    show_corrected_command(cmd)
    out, err = capsys.readouterr()
    # stderr should contain the formatted command with side effect
    expected = f"{const.USER_COMMAND_MARK}{color(colorama.Style.BRIGHT)}{cmd.script}{color(colorama.Style.RESET_ALL)} (+side effect)\n"
    assert err == expected
    assert out == ""

def test_show_corrected_command_without_side_effect(capsys, monkeypatch):
    # Ensure colors are enabled
    monkeypatch.setattr('thefuck.conf.settings.no_colors', False)
    cmd = DummyCommand('git status', side_effect=False)
    show_corrected_command(cmd)
    out, err = capsys.readouterr()
    expected = f"{const.USER_COMMAND_MARK}{color(colorama.Style.BRIGHT)}{cmd.script}{color(colorama.Style.RESET_ALL)}\n"
    assert err == expected
    assert out == ""

def test_show_corrected_command_no_colors(capsys, monkeypatch):
    # Disable colors
    monkeypatch.setattr('thefuck.conf.settings.no_colors', True)
    cmd = DummyCommand('echo hello', side_effect=False)
    show_corrected_command(cmd)
    out, err = capsys.readouterr()
    # When colors are disabled, color() returns empty string
    expected = f"{const.USER_COMMAND_MARK}{cmd.script}\n"
    assert err == expected
    assert out == ""
