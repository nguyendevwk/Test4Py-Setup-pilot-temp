import os
import zipfile
import tempfile
import shutil
import pytest

from thefuck.rules.dirty_unzip import match, _zip_file, _is_bad_zip


class DummyCommand:
    def __init__(self, script: str):
        self.script = script


def create_valid_zip(path: str):
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("file.txt", "content")


def create_corrupted_zip(path: str):
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("file.txt", "content")
    # Truncate the file to corrupt it
    with open(path, "rb+") as f:
        f.truncate(10)


def test_match_with_valid_zip_returns_false(tmp_path):
    zip_path = tmp_path / "valid.zip"
    create_valid_zip(str(zip_path))
    cmd = DummyCommand(f"unzip {zip_path}")
    assert match(cmd) is False


def test_match_with_corrupted_zip_returns_true(tmp_path):
    zip_path = tmp_path / "bad.zip"
    create_corrupted_zip(str(zip_path))
    cmd = DummyCommand(f"unzip {zip_path}")
    assert match(cmd) is True


def test_match_with_d_flag_returns_false(tmp_path):
    zip_path = tmp_path / "valid.zip"
    create_valid_zip(str(zip_path))
    cmd = DummyCommand(f"unzip -d {zip_path}")
    assert match(cmd) is False
