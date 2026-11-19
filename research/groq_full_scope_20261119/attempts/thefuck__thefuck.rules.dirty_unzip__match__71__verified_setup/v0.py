import os
import zipfile
import tempfile
import shutil
import pytest

from thefuck.rules.dirty_unzip import match


def _create_zip(path, bad=False):
    """Create a zip file at `path`. If `bad` is True, truncate the file to make it invalid."""
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr('test.txt', 'content')
    if bad:
        # Truncate the file to corrupt it
        with open(path, 'ab') as f:
            f.truncate(10)


class DummyCommand:
    """Simple command object with a `script` attribute."""
    def __init__(self, script):
        self.script = script


def test_match_with_d_flag(tmp_path):
    """When the script contains '-d', match should return False regardless of zip file."""
    zip_path = tmp_path / "archive.zip"
    _create_zip(zip_path)
    cmd = DummyCommand(f"unzip -d {zip_path}")
    assert match(cmd) is False


def test_match_without_zip_file(tmp_path):
    """When the script does not reference a zip file, match should return False."""
    cmd = DummyCommand("unzip somefile.txt")
    assert match(cmd) is False


def test_match_with_bad_zip(tmp_path):
    """When the script references a corrupted zip file, match should return True."""
    bad_zip_path = tmp_path / "bad.zip"
    _create_zip(bad_zip_path, bad=True)
    cmd = DummyCommand(f"unzip {bad_zip_path}")
    assert match(cmd) is True
