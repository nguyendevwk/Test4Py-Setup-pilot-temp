import builtins
import json
import os
import tempfile
import time
import getpass
import pytest
from pathlib import Path

# Import the module under test
from thefuck.entrypoints import not_configured

# Helper to create a fake configuration details object
class FakeConfig:
    def __init__(self, path, content, can_configure=True):
        self.path = path
        self.content = content
        self.can_configure_automatically = can_configure

# Test scenario 1: First run – no prior configuration, not second run
def test_main_first_run(tmp_path, monkeypatch):
    # Prepare fake configuration details
    config_path = tmp_path / "shellrc"
    config_path.write_text("")  # empty shell config
    fake_conf = FakeConfig(str(config_path), "alias fuck='echo configured'")

    # Patch dependencies
    monkeypatch.setattr(not_configured.settings, "init", lambda: None)
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: fake_conf)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda x: False)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)
    monkeypatch.setattr(not_configured, "_configure", lambda x: None)
    called = {}
    def record_first_run():
        called["recorded"] = True
    monkeypatch.setattr(not_configured, "_record_first_run", record_first_run)
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", lambda x: None)
    monkeypatch.setattr(not_configured.logs, "already_configured", lambda x: None)
    monkeypatch.setattr(not_configured.logs, "configured_successfully", lambda x: None)

    # Run main
    not_configured.main()

    # Assertions
    assert called.get("recorded") is True
    # Ensure no configure or logs for configured
    assert not hasattr(called, "configured")

# Test scenario 2: Second run – should configure automatically
def test_main_second_run(tmp_path, monkeypatch):
    config_path = tmp_path / "shellrc"
    config_path.write_text("")  # empty shell config
    fake_conf = FakeConfig(str(config_path), "alias fuck='echo configured'")

    monkeypatch.setattr(not_configured.settings, "init", lambda: None)
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: fake_conf)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda x: False)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: True)
    called = {}
    def configure(x):
        called["configured"] = True
    monkeypatch.setattr(not_configured, "_configure", configure)
    monkeypatch.setattr(not_configured, "_record_first_run", lambda: None)
    monkeypatch.setattr(not_configured.logs, "configured_successfully", lambda x: None)
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", lambda x: None)
    monkeypatch.setattr(not_configured.logs, "already_configured", lambda x: None)

    not_configured.main()

    assert called.get("configured") is True

# Test scenario 3: Already configured – should log already configured
def test_main_already_configured(tmp_path, monkeypatch):
    config_path = tmp_path / "shellrc"
    config_path.write_text("alias fuck='echo configured'")  # already contains alias
    fake_conf = FakeConfig(str(config_path), "alias fuck='echo configured'")

    monkeypatch.setattr(not_configured.settings, "init", lambda: None)
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: fake_conf)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda x: True)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)
    monkeypatch.setattr(not_configured, "_configure", lambda x: None)
    monkeypatch.setattr(not_configured, "_record_first_run", lambda: None)
    called = {}
    monkeypatch.setattr(not_configured.logs, "already_configured", lambda x: called.setdefault("already", True))
    monkeypatch.setattr(not_configured.logs, "configured_successfully", lambda x: None)
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", lambda x: None)

    not_configured.main()

    assert called.get("already") is True
