import sys
import pytest
from mimesis.providers.path import Path
from pathlib import PurePosixPath, PureWindowsPath

def test_root_and_home_on_linux():
    """Verify that root and home paths are correct for a Linux platform."""
    provider = Path(platform="linux")
    # root should be the parent of the home directory
    expected_root = str(PurePosixPath("/").parent)  # "/"
    assert provider.root() == expected_root
    # home should be /home
    assert provider.home() == "/home"

def test_user_path_case_on_windows():
    """Ensure Windows user paths are capitalized and use backslashes."""
    provider = Path(platform="win32")
    user_path = provider.user()
    # The path should start with the Windows home directory
    assert user_path.startswith(str(PureWindowsPath("C:\\Users")))
    # The username part should be capitalized
    username = user_path.split("\\")[-1]
    assert username[0].isupper()
    # The path should use backslashes
    assert "\\" in user_path

def test_dev_dir_and_project_dir_randomness():
    """Check that dev_dir and project_dir produce distinct, valid paths."""
    provider = Path(platform="linux")
    dev_dir1 = provider.dev_dir()
    dev_dir2 = provider.dev_dir()
    # dev_dir should contain a programming language and a dev folder
    assert any(lang in dev_dir1 for lang in provider.random.choice.__self__.datasets.PROGRAMMING_LANGS)
    assert any(folder in dev_dir1 for folder in ["Development", "Dev"])
    # Two consecutive calls should not always return the same path
    assert dev_dir1 != dev_dir2
    # project_dir should append a project name to the dev_dir
    project_dir = provider.project_dir()
    assert project_dir.startswith(dev_dir1)
    project_name = project_dir.split("/")[-1]
    assert project_name in provider.random.choice.__self__.datasets.PROJECT_NAMES
