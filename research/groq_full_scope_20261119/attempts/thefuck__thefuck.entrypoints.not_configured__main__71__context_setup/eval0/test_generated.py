import json
import os
import time
import getpass
import tempfile
import pytest
from pathlib import Path

# Import the module under test
from thefuck.entrypoints import not_configured

# Helper to create a fake configuration_details object
class DummyConfig:
    def __init__(self, path, content, can_configure_automatically=True):
        self.path = path
        self.content = content
        self.can_configure_automatically = can_configure_automatically

def test_is_already_configured(tmp_path):
    """Verify that _is_already_configured detects existing alias."""
    # Create a temporary shell config file
    config_file = tmp_path / ".bashrc"
    config_file.write_text("alias fuck='echo fuck'\n")
    cfg = DummyConfig(path=str(config_file), content="alias fuck='echo fuck'")
    # Should return True because content exists
    assert not_configured._is_already_configured(cfg) is True

    # Remove the content and test again
    config_file.write_text("alias something='echo'\n")
    assert not_configured._is_already_configured(cfg) is False

def test_record_and_second_run(tmp_path, monkeypatch):
    """Ensure that recording a first run and detecting a second run works."""
    # Patch the tracker path to use a temp file
    tracker = tmp_path / "tracker.json"
    monkeypatch.setattr(not_configured, "_get_not_configured_usage_tracker_path",
                       lambda: tracker)

    # Ensure no tracker exists initially
    assert not tracker.exists()

    # Record first run
    not_configured._record_first_run()
    assert tracker.exists()
    with tracker.open() as f:
        data = json.load(f)
    assert "pid" in data and "time" in data
    first_pid = data["pid"]
    first_time = data["time"]

    # Simulate same shell process by patching _get_shell_pid
    monkeypatch.setattr(not_configured, "_get_shell_pid", lambda: first_pid)

    # Patch _get_previous_command to return 'fuck'
    monkeypatch.setattr(not_configured, "_get_previous_command", lambda: "fuck")

    # Immediately check second run detection
    assert not_configured._is_second_run() is True

    # Simulate time passing beyond timeout
    monkeypatch.setattr(time, "time", lambda: first_time + not_configured.const.CONFIGURATION_TIMEOUT + 1)
    assert not_configured._is_second_run() is False

def test_main_behavior(tmp_path, monkeypatch, capsys):
    """Test that main logs the correct message when alias is not configured."""
    # Create a dummy shell config file without the alias
    config_file = tmp_path / ".bashrc"
    config_file.write_text("alias something='echo'\n")
    cfg = DummyConfig(path=str(config_file), content="alias fuck='echo fuck'")

    # Patch shell.how_to_configure to return our dummy config
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: cfg)

    # Patch _is_already_configured to return False
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda x: False)

    # Patch _is_second_run to return False so that first run path is taken
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)

    # Patch _record_first_run to do nothing
    monkeypatch.setattr(not_configured, "_record_first_run", lambda: None)

    # Patch logs.how_to_configure_alias to capture the message
    messages = []
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias",
                       lambda cfg: messages.append(f"Configure alias: {cfg.content}"))

    # Run main
    not_configured.main()

    # Verify that the configure alias message was logged
    assert messages == [f"Configure alias: {cfg.content}"]

    # Ensure no other output was printed
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
