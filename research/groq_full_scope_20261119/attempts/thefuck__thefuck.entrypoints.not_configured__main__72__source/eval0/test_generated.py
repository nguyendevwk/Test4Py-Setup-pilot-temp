import builtins
import os
import json
import importlib
import types
import pytest

# Import the module under test
from thefuck.entrypoints import not_configured

# Helper to create a fake configuration_details object
class FakeConfig:
    def __init__(self, can_configure_automatically=True):
        self.can_configure_automatically = can_configure_automatically

# Test 1: First run – should record first run and not configure
def test_main_first_run(tmp_path, monkeypatch):
    # Patch gettempdir to use tmp_path
    monkeypatch.setattr(not_configured, "gettempdir", lambda: str(tmp_path))
    # Patch settings.init to do nothing
    monkeypatch.setattr(not_configured.settings, "init", lambda: None)
    # Patch shell.how_to_configure to return a config that can configure automatically
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: FakeConfig())
    # Patch helper functions to return False for already configured and second run
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda cfg: False)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)
    # Patch _configure to raise if called
    monkeypatch.setattr(not_configured, "_configure", lambda cfg: (_ for _ in ()).throw(RuntimeError("Should not configure on first run")))
    # Patch logs functions to track calls
    called = {}
    def log_how(cfg):
        called["how"] = True
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", log_how)
    # Run main
    not_configured.main()
    # Verify that the first run file was created
    first_run_file = os.path.join(str(tmp_path), "thefuck_first_run")
    assert os.path.exists(first_run_file)
    # Verify that the correct log was called
    assert called.get("how") is True

# Test 2: Second run – should configure automatically
def test_main_second_run(tmp_path, monkeypatch):
    monkeypatch.setattr(not_configured, "gettempdir", lambda: str(tmp_path))
    monkeypatch.setattr(not_configured.settings, "init", lambda: None)
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: FakeConfig())
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda cfg: False)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: True)
    # Track configuration call
    called = {}
    def configure(cfg):
        called["configured"] = True
    monkeypatch.setattr(not_configured, "_configure", configure)
    # Patch logs to track calls
    monkeypatch.setattr(not_configured.logs, "configured_successfully", lambda cfg: called.setdefault("log_configured", True))
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", lambda cfg: (_ for _ in ()).throw(RuntimeError("Should not log how to configure on second run")))
    # Run main
    not_configured.main()
    # Verify that configuration was performed
    assert called.get("configured") is True
    assert called.get("log_configured") is True

# Test 3: Already configured – should log already configured and exit
def test_main_already_configured(monkeypatch):
    monkeypatch.setattr(not_configured.settings, "init", lambda: None)
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: FakeConfig())
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda cfg: True)
    # Patch _is_second_run and _configure to raise if called
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: (_ for _ in ()).throw(RuntimeError("Should not check second run")))
    monkeypatch.setattr(not_configured, "_configure", lambda cfg: (_ for _ in ()).throw(RuntimeError("Should not configure")))
    # Track logs
    called = {}
    def log_already(cfg):
        called["already"] = True
    monkeypatch.setattr(not_configured.logs, "already_configured", log_already)
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", lambda cfg: (_ for _ in ()).throw(RuntimeError("Should not log how to configure")))
    # Run main
    not_configured.main()
    # Verify that already_configured was logged
    assert called.get("already") is True
