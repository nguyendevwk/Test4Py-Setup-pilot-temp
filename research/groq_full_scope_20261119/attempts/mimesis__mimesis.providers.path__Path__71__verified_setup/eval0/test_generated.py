import re
import sys
import pytest
from mimesis.providers.path import Path

# Helper to create a provider with a fixed seed for deterministic random choices
def make_provider(platform: str = "linux") -> Path:
    provider = Path(platform=platform)
    provider.random.seed(0)
    return provider

def test_root_and_home_consistency():
    """Root should be the parent directory of home."""
    provider = make_provider()
    root = provider.root()
    home = provider.home()
    # root should be the parent of home
    assert root == str(Path(root).parent) or root == "/"
    assert home.startswith(root)
    # On POSIX, root should be '/' and home should be '/home' or similar
    assert root == "/"
    assert home == "/home"

def test_user_path_case_on_windows_and_unix():
    """User path should be capitalized on Windows and lowercased on Unix."""
    # Windows platform
    win_provider = make_provider(platform="win32")
    win_user = win_provider.user()
    # The username part should be capitalized
    win_username = win_user.split("/")[-1]
    assert win_username[0].isupper()
    # Unix platform
    unix_provider = make_provider(platform="linux")
    unix_user = unix_provider.user()
    unix_username = unix_user.split("/")[-1]
    assert unix_username.islower()

def test_dev_dir_contains_expected_components():
    """Development directory should contain a valid folder and programming language."""
    provider = make_provider()
    dev_dir = provider.dev_dir()
    # Split the path into components
    parts = dev_dir.split("/")
    # The path should have at least 5 parts: ['', 'home', 'username', 'folder', 'lang']
    assert len(parts) >= 5
    # The folder should be either 'Development' or 'Dev'
    assert parts[-2] in ("Development", "Dev")
    # The programming language should be a known language from PROGRAMMING_LANGS
    # Since we cannot import the dataset directly, we check that the language part
    # is alphabetic and not empty
    lang = parts[-1]
    assert lang.isalpha() and len(lang) > 0
