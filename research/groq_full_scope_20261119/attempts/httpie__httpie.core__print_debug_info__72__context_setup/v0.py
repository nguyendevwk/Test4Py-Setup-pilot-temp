import io
import os
import sys
import platform
import pytest
from httpie.core import print_debug_info
from httpie.context import Environment
from httpie.plugins.registry import plugin_manager

@pytest.fixture
def env_with_file(tmp_path):
    """Create an Environment that writes to a temporary file."""
    file_path = tmp_path / "stderr.txt"
    file_obj = open(file_path, "w", encoding="utf-8")
    env = Environment(stderr=file_obj)
    yield env, file_path
    file_obj.close()

def test_print_debug_info_includes_expected_sections(env_with_file):
    env, file_path = env_with_file
    print_debug_info(env)
    env.stderr.flush()
    content = file_path.read_text(encoding="utf-8")

    # Check that each expected header appears
    assert f"HTTPie {env.httpie_version}" in content
    assert f"Requests {env.requests_version}" in content
    assert f"Pygments {env.pygments_version}" in content
    assert f"Python {sys.version}" in content
    assert sys.executable in content
    assert f"{platform.system()} {platform.release()}" in content

    # Environment representation should be present
    assert repr(env) in content

    # Plugin manager representation should be present
    assert repr(plugin_manager) in content

def test_print_debug_info_separates_sections(env_with_file):
    env, file_path = env_with_file
    print_debug_info(env)
    env.stderr.flush()
    content = file_path.read_text(encoding="utf-8")

    # Ensure there are exactly two blank lines after the system info block
    lines = content.splitlines()
    # Find the index of the first empty line after system info
    first_empty = next(i for i, l in enumerate(lines) if l.strip() == "")
    # The next line should also be empty
    assert lines[first_empty + 1].strip() == ""

    # Ensure that after the environment repr there are two blank lines
    env_repr_index = lines.index(repr(env))
    assert lines[env_repr_index + 1].strip() == ""
    assert lines[env_repr_index + 2].strip() == ""

def test_print_debug_info_raises_on_invalid_stderr(env_with_file):
    env, file_path = env_with_file
    # Close the file to simulate a broken stderr
    env.stderr.close()
    with pytest.raises(ValueError):
        print_debug_info(env)
