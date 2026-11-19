import os
import json
import builtins
import importlib
import tempfile
import pytest

# Import the module under test
from thefuck.entrypoints import not_configured

# Helper to create a fake configuration_details object
class FakeConfig:
    def __init__(self, can_configure_automatically=True):
        self.can_configure_automatically = can_configure_automatically

@pytest.fixture
def monkeypatch_module(monkeypatch):
    """Patch the module's dependencies for controlled testing."""
    # Patch settings.init to do nothing
    monkeypatch.setattr(not_configured.settings, "init", lambda: None)

    # Patch shell.how_to_configure to return a fake config
    monkeypatch.setattr(not_configured.shell, "how_to_configure", lambda: FakeConfig())

    # Patch logs functions to no-ops
    monkeypatch.setattr(not_configured.logs, "already_configured", lambda *_, **__: None)
    monkeypatch.setattr(not_configured.logs, "configured_successfully", lambda *_, **__: None)
    monkeypatch.setattr(not_configured.logs, "how_to_configure_alias", lambda *_, **__: None)

    # Patch _record_first_run to write to a known temp file
    temp_file = os.path.join(tempfile.gettempdir(), "thefuck_first_run_flag")
    if os.path.exists(temp_file):
        os.remove(temp_file)
    monkeypatch.setattr(not_configured, "_record_first_run", lambda: open(temp_file, "w").close())
    return temp_file

def test_first_run_creates_flag(monkeypatch_module):
    """When it is the first run, a flag file should be created."""
    temp_file = monkeypatch_module

    # Ensure the flag file does not exist before running
    assert not os.path.exists(temp_file)

    # Patch _is_second_run to False and _is_already_configured to False
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda _: False)

    # Run main
    not_configured.main()

    # After first run, the flag file should exist
    assert os.path.exists(temp_file)

def test_second_run_configures_and_logs(monkeypatch_module):
    """On the second run, configuration should be performed."""
    temp_file = monkeypatch_module

    # Create the flag file to simulate first run already happened
    open(temp_file, "w").close()

    # Patch _is_second_run to True and _is_already_configured to False
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: True)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda _: False)

    # Patch _configure to record that it was called
    called = {"configured": False}
    def fake_configure(details):
        called["configured"] = True
    monkeypatch.setattr(not_configured, "_configure", fake_configure)

    # Run main
    not_configured.main()

    # Verify that configuration was performed
    assert called["configured"] is True

def test_already_configured_logs_only(monkeypatch_module):
    """If already configured, only the already_configured log should be called."""
    temp_file = monkeypatch_module

    # Ensure flag file exists
    open(temp_file, "w").close()

    # Patch _is_second_run to False and _is_already_configured to True
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda _: True)

    # Patch logs.already_configured to record call
    called = {"already": False}
    monkeypatch.setattr(not_configured.logs, "already_configured", lambda details: called.update({"already": True}))

    # Run main
    not_configured.main()

    # Verify that only the already_configured log was called
    assert called["already"] is True
