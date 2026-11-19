import re
import sys
import pytest
from mimesis.providers.path import Path

def test_path_root_and_home_on_linux(tmp_path):
    """Verify that root and home are correct for a Linux platform."""
    p = Path(platform="linux")
    # root should be the parent of the home directory
    assert p.root() == "/"
    # home should be the configured home directory
    assert p.home() == "/home"

def test_user_path_case_on_windows(tmp_path):
    """Ensure Windows user paths are capitalized and use backslashes."""
    p = Path(platform="win32")
    user_path = p.user()
    # Windows home should start with a drive letter and backslash
    assert re.match(r"^[A-Za-z]:\\", user_path)
    # The username part should be capitalized
    username = user_path.split("\\")[-1]
    assert username[0].isupper()
    assert username == username.capitalize()

def test_dev_and_project_dir_structure(tmp_path):
    """Check that dev_dir and project_dir contain expected components."""
    p = Path(platform="linux")
    dev = p.dev_dir()
    # dev_dir should contain /Development/ or /Dev/ and a programming language
    assert re.search(r"/(Development|Dev)/[A-Za-z]+$", dev)
    proj = p.project_dir()
    # project_dir should extend dev_dir with a project name
    assert proj.startswith(dev)
    assert proj != dev  # ensure a project name is appended
    # The project name should be one of the known project names
    project_name = proj.split("/")[-1]
    assert project_name in p.random.choice.__self__.datasets.PROJECT_NAMES
