import sys
import pytest
from pathlib import PurePosixPath, PureWindowsPath
from mimesis.providers.path import Path
from mimesis.datasets import PLATFORMS, USERNAMES, FOLDERS, PROGRAMMING_LANGS, PROJECT_NAMES

def test_posix_root_and_home():
    """Verify that root and home paths are correct for a POSIX platform."""
    provider = Path(platform="linux")
    # root should be the parent of the home directory
    expected_root = str(PurePosixPath(PLATFORMS["linux"]["home"]).parent)
    assert provider.root() == expected_root
    # home should match the configured home directory
    expected_home = str(PurePosixPath(PLATFORMS["linux"]["home"]))
    assert provider.home() == expected_home

def test_windows_user_path_and_case():
    """Verify that Windows user paths are capitalized and use backslashes."""
    provider = Path(platform="win32")
    user_path = provider.user()
    # The path should start with the Windows home directory
    expected_home = str(PureWindowsPath(PLATFORMS["win32"]["home"]))
    assert user_path.startswith(expected_home)
    # The username part should be capitalized
    username = user_path.split(expected_home)[-1].strip("\\")
    assert username[0].isupper()
    # Ensure backslashes are used in the path
    assert "\\" in user_path

def test_dev_dir_contains_folder_and_language():
    """Verify that dev_dir includes a development folder and a programming language."""
    provider = Path(platform="darwin")
    dev_path = provider.dev_dir()
    # Split the path and check components
    parts = dev_path.split("/")
    # The second component should be a username (lowercase)
    username = parts[1]
    assert username.islower()
    # The third component should be either Development or Dev
    assert parts[2] in ("Development", "Dev")
    # The fourth component should be a programming language from the dataset
    assert parts[3] in PROGRAMMING_LANGS
