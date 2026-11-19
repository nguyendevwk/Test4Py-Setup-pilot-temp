import os
import zipfile
import pytest
from thefuck.rules.dirty_unzip import side_effect

@pytest.fixture
def zip_path(tmp_path):
    """Create a zip file containing one safe and one unsafe file."""
    safe_file = tmp_path / "safe.txt"
    safe_file.write_text("safe")
    unsafe_file = tmp_path.parent / "outside.txt"
    unsafe_file.write_text("outside")
    zpath = tmp_path / "archive.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        z.write(safe_file, arcname="safe.txt")
        z.write(unsafe_file, arcname="../outside.txt")
    return zpath

def test_removal_of_safe_files(tmp_path, zip_path, monkeypatch):
    """Files inside the current directory are removed."""
    # Ensure the safe file exists before the call
    safe_file = tmp_path / "safe.txt"
    assert safe_file.exists()
    # Monkeypatch _zip_file to return our test zip
    monkeypatch.setattr("thefuck.rules.dirty_unzip._zip_file", lambda old_cmd: str(zip_path))
    # Call side_effect with a dummy command
    side_effect("unzip archive.zip", None)
    # The safe file should be removed
    assert not safe_file.exists()

def test_skipping_unsafe_files(tmp_path, zip_path, monkeypatch):
    """Files outside the current directory are not removed."""
    unsafe_file = tmp_path.parent / "outside.txt"
    assert unsafe_file.exists()
    monkeypatch.setattr("thefuck.rules.dirty_unzip._zip_file", lambda old_cmd: str(zip_path))
    side_effect("unzip archive.zip", None)
    # The unsafe file should still exist
    assert unsafe_file.exists()

def test_handling_oserror(tmp_path, zip_path, monkeypatch):
    """OSError during removal is ignored and does not propagate."""
    safe_file = tmp_path / "safe.txt"
    assert safe_file.exists()
    # Monkeypatch os.remove to raise OSError for the safe file
    def fake_remove(path):
        if os.path.abspath(path) == os.path.abspath(safe_file):
            raise OSError("simulated error")
        os.remove(path)
    monkeypatch.setattr("thefuck.rules.dirty_unzip.os.remove", fake_remove)
    monkeypatch.setattr("thefuck.rules.dirty_unzip._zip_file", lambda old_cmd: str(zip_path))
    # side_effect should not raise
    side_effect("unzip archive.zip", None)
    # The safe file should still exist because removal failed
    assert safe_file.exists()
