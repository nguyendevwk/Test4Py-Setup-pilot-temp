import sys
import pytest
from mimesis.providers.path import Path
from pathlib import PurePosixPath, PureWindowsPath

def test_path_linux_behavior(tmp_path):
    """Verify that Path on a Linux platform returns expected POSIX paths."""
    p = Path(platform="linux")
    # root should be parent of home
    assert p.root() == str(PurePosixPath(p.home()).parent)
    # home should end with the platform-specific home directory
    assert p.home().endswith("/home")
    # user should be lowercase and under home
    user_path = p.user()
    assert user_path.startswith(p.home() + "/")
    assert user_path.split("/")[-1].islower()
    # users_folder should be a subfolder of the user path
    folder_path = p.users_folder()
    assert folder_path.startswith(user_path + "/")
    # dev_dir should contain a programming language stack
    dev_path = p.dev_dir()
    assert dev_path.startswith(user_path + "/")
    assert any(stack in dev_path for stack in ["Development", "Dev"])
    # project_dir should append a project name
    proj_path = p.project_dir()
    assert proj_path.startswith(dev_path + "/")
    assert any(name in proj_path for name in ["mercenary", "falcon", "project"])


def test_path_windows_behavior(tmp_path):
    """Verify that Path on a Windows platform returns expected Windows paths."""
    p = Path(platform="win32")
    # root should be parent of home
    assert p.root() == str(PureWindowsPath(p.home()).parent)
    # home should end with the platform-specific home directory
    assert p.home().endswith("\\Users")
    # user should be capitalized and under home
    user_path = p.user()
    assert user_path.startswith(p.home() + "\\")
    assert user_path.split("\\")[-1].istitle()
    # users_folder should be a subfolder of the user path
    folder_path = p.users_folder()
    assert folder_path.startswith(user_path + "\\")
    # dev_dir should contain a programming language stack
    dev_path = p.dev_dir()
    assert dev_path.startswith(user_path + "\\")
    assert any(stack in dev_path for stack in ["Development", "Dev"])
    # project_dir should append a project name
    proj_path = p.project_dir()
    assert proj_path.startswith(dev_path + "\\")
    assert any(name in proj_path for name in ["mercenary", "falcon", "project"])


def test_invalid_platform_raises():
    """Providing an unsupported platform should raise a KeyError."""
    with pytest.raises(KeyError):
        Path(platform="unsupported_platform")
