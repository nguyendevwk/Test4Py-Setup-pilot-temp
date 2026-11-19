import sys
import importlib
import types
import os
import pathlib

import pytest

# Import the target function and related classes
from thefuck.corrector import get_rules_import_paths
from thefuck.system import Path
from thefuck.conf import settings


@pytest.fixture
def restore_sys_path():
    original = sys.path.copy()
    yield
    sys.path[:] = original


@pytest.fixture
def restore_user_dir():
    original = settings.user_dir
    yield
    settings.user_dir = original


def test_bundled_and_user_paths(tmp_path, restore_sys_path, restore_user_dir):
    """The first two yielded paths are the bundled rules directory and the user rules directory."""
    # Set user_dir to a temporary directory
    settings.user_dir = tmp_path

    # Call the generator and collect results
    paths = list(get_rules_import_paths())

    # The bundled rules path should be a subdirectory of this module's directory
    bundled = Path(__file__).parent.joinpath('rules')
    assert paths[0] == bundled
    # The user rules path should be the tmp_path joined with 'rules'
    assert paths[1] == tmp_path.joinpath('rules')


def test_contrib_with_rules(tmp_path, restore_sys_path, restore_user_dir):
    """Contrib modules that contain a 'rules' subdirectory are yielded."""
    # Create a dummy contrib module directory with a 'rules' subdirectory
    contrib_dir = tmp_path / "thefuck_contrib_example"
    contrib_dir.mkdir()
    rules_dir = contrib_dir / "rules"
    rules_dir.mkdir()

    # Add the temporary directory to sys.path
    sys.path.insert(0, str(tmp_path))

    # Call the generator and collect results
    paths = list(get_rules_import_paths())

    # The contrib rules directory should be in the list
    assert rules_dir in paths
    # Ensure that the contrib path appears after the bundled and user paths
    bundled = Path(__file__).parent.joinpath('rules')
    user_rules = settings.user_dir.joinpath('rules')
    assert paths.index(rules_dir) > paths.index(bundled)
    assert paths.index(rules_dir) > paths.index(user_rules)


def test_contrib_without_rules(tmp_path, restore_sys_path, restore_user_dir):
    """Contrib modules without a 'rules' subdirectory are not yielded."""
    # Create a dummy contrib module directory without a 'rules' subdirectory
    contrib_dir = tmp_path / "thefuck_contrib_norules"
    contrib_dir.mkdir()

    # Add the temporary directory to sys.path
    sys.path.insert(0, str(tmp_path))

    # Call the generator and collect results
    paths = list(get_rules_import_paths())

    # The contrib directory without 'rules' should not be in the list
    assert contrib_dir.joinpath('rules') not in paths
