import sys
import pathlib
import pytest
from mimesis.providers.path import Path

# Helper to set a deterministic seed for the provider's random generator
def _seed_provider(provider, seed=0):
    provider.random.seed(seed)

@pytest.mark.parametrize("platform,expected_home_prefix", [
    ("linux", "/home"),
    ("darwin", "/Users"),
    ("win32", "C:\\Users"),
    ("win64", "C:\\Users"),
    ("freebsd", "/home"),
])
def test_path_basic(platform, expected_home_prefix):
    """Verify that root, home, and user paths are constructed correctly for various platforms."""
    provider = Path(platform=platform)
    _seed_provider(provider, seed=42)

    # Root should be the parent directory of home
    root = provider.root()
    home = provider.home()
    assert pathlib.PurePath(home).parent == pathlib.PurePath(root)

    # Home should start with the expected prefix
    assert home.startswith(expected_home_prefix)

    # User path should be a subpath of home
    user_path = provider.user()
    assert pathlib.PurePath(user_path).is_relative_to(home)

    # On Windows platforms, username should be capitalized
    if platform.startswith("win"):
        username = pathlib.PurePath(user_path).parts[-1]
        assert username[0].isupper()
    else:
        username = pathlib.PurePath(user_path).parts[-1]
        assert username.islower()


def test_users_folder_and_dev_dir_structure():
    """Ensure that users_folder and dev_dir produce nested paths under the user's home."""
    provider = Path(platform="linux")
    _seed_provider(provider, seed=123)

    user_path = provider.user()
    users_folder = provider.users_folder()
    dev_dir = provider.dev_dir()

    # users_folder should be user_path / folder
    assert pathlib.PurePath(users_folder).parts[:2] == pathlib.PurePath(user_path).parts[:2]
    # dev_dir should be user_path / (Development|Dev) / language
    dev_parts = pathlib.PurePath(dev_dir).parts
    assert dev_parts[0] == pathlib.PurePath(user_path).parts[0]
    assert dev_parts[1] == pathlib.PurePath(user_path).parts[1]
    assert dev_parts[2] in ("Development", "Dev")
    assert dev_parts[3] in provider.random.choice.__self__.datasets.PROGRAMMING_LANGS


def test_project_dir_includes_dev_and_project_names():
    """Check that project_dir contains the dev directory and a project name."""
    provider = Path(platform="darwin")
    _seed_provider(provider, seed=7)

    dev_dir = provider.dev_dir()
    project_dir = provider.project_dir()

    # project_dir should start with dev_dir
    assert pathlib.PurePath(project_dir).is_relative_to(dev_dir)

    # The last component of project_dir should be a project name
    project_name = pathlib.PurePath(project_dir).parts[-1]
    assert project_name in provider.random.choice.__self__.datasets.PROJECT_NAMES
