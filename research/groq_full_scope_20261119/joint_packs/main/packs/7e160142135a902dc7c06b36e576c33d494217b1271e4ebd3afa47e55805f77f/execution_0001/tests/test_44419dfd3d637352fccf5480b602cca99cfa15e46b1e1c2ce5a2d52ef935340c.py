import types
import pytest

# Import the module under test
from thefuck.entrypoints import not_configured

@pytest.fixture
def mock_shell():
    """Create a mock shell object with required attributes."""
    mock = types.SimpleNamespace()
    mock.can_configure_automatically = True
    return mock

@pytest.fixture
def mock_logs():
    """Create a mock logs object with methods that record calls."""
    class Logger:
        def __init__(self):
            self.calls = []

        def already_configured(self, *args, **kwargs):
            self.calls.append(("already_configured", args, kwargs))

        def configured_successfully(self, *args, **kwargs):
            self.calls.append(("configured_successfully", args, kwargs))

        def how_to_configure_alias(self, *args, **kwargs):
            self.calls.append(("how_to_configure_alias", args, kwargs))

    return Logger()

def test_first_run(monkeypatch, mock_shell, mock_logs):
    """When the alias is not configured and this is the first run,
    the function should record the first run and show the configuration guide."""
    # Patch dependencies
    monkeypatch.setattr(not_configured, "settings", types.SimpleNamespace(init=lambda: None))
    monkeypatch.setattr(not_configured, "shell", types.SimpleNamespace(how_to_configure=lambda: mock_shell))
    monkeypatch.setattr(not_configured, "logs", mock_logs)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda cfg: False)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: False)
    monkeypatch.setattr(not_configured, "_record_first_run", lambda: None)

    # Call the function
    not_configured.main()

    # Verify that the first run was recorded and the guide was shown
    assert ("how_to_configure_alias", (mock_shell,), {}) in mock_logs.calls
    assert ("already_configured", (mock_shell,), {}) not in mock_logs.calls
    assert ("configured_successfully", (mock_shell,), {}) not in mock_logs.calls

def test_second_run(monkeypatch, mock_shell, mock_logs):
    """When the alias is not configured and this is the second run,
    the function should configure automatically and log success."""
    monkeypatch.setattr(not_configured, "settings", types.SimpleNamespace(init=lambda: None))
    monkeypatch.setattr(not_configured, "shell", types.SimpleNamespace(how_to_configure=lambda: mock_shell))
    monkeypatch.setattr(not_configured, "logs", mock_logs)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda cfg: False)
    monkeypatch.setattr(not_configured, "_is_second_run", lambda: True)
    monkeypatch.setattr(not_configured, "_configure", lambda cfg: None)

    not_configured.main()

    assert ("configured_successfully", (mock_shell,), {}) in mock_logs.calls
    assert ("how_to_configure_alias", (mock_shell,), {}) not in mock_logs.calls
    assert ("already_configured", (mock_shell,), {}) not in mock_logs.calls

def test_already_configured(monkeypatch, mock_shell, mock_logs):
    """When the alias is already configured, the function should log that and exit."""
    monkeypatch.setattr(not_configured, "settings", types.SimpleNamespace(init=lambda: None))
    monkeypatch.setattr(not_configured, "shell", types.SimpleNamespace(how_to_configure=lambda: mock_shell))
    monkeypatch.setattr(not_configured, "logs", mock_logs)
    monkeypatch.setattr(not_configured, "_is_already_configured", lambda cfg: True)

    not_configured.main()

    assert ("already_configured", (mock_shell,), {}) in mock_logs.calls
    assert ("configured_successfully", (mock_shell,), {}) not in mock_logs.calls
    assert ("how_to_configure_alias", (mock_shell,), {}) not in mock_logs.calls
