import sys
import os
import pytest
from httpie.core import main
from httpie.status import ExitStatus
from httpie.context import Environment
from httpie.cli.constants import OUT_REQ_BODY

@pytest.fixture
def env(tmp_path):
    """Create a clean Environment with a temporary config directory."""
    env = Environment()
    env.config_dir = tmp_path
    env.config = {"default_options": []}
    return env

def test_main_success_offline(env, capsys):
    """Running httpie with --offline should succeed without network."""
    # Use a harmless URL that would normally succeed
    args = ["-c", "--offline", "https://httpbin.org/get"]
    status = main(args=args, env=env)
    assert status == ExitStatus.SUCCESS
    # Ensure no error messages were printed
    out, err = capsys.readouterr()
    assert err == ""

def test_main_invalid_url_offline(env, capsys):
    """Providing an invalid URL should return an error status."""
    args = ["-c", "--offline", "http://invalid_url"]
    status = main(args=args, env=env)
    assert status == ExitStatus.ERROR
    out, err = capsys.readouterr()
    # Error message should mention the URL
    assert "invalid_url" in err

def test_main_debug_info(env, capsys):
    """The --debug flag should print debug information and exit with SUCCESS."""
    args = ["-c", "--debug"]
    status = main(args=args, env=env)
    assert status == ExitStatus.SUCCESS
    out, err = capsys.readouterr()
    # Debug output should contain version info and environment repr
    assert "HTTPie" in out
    assert "Requests" in out
    assert "Pygments" in out
    assert "Python" in out
    assert repr(env) in out
