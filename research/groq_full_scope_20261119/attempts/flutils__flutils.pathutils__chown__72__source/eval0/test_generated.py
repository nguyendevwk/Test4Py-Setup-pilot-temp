import os
import getpass
import pwd
import grp
import pytest
from pathlib import Path
from flutils.pathutils import chown, normalize_path


def test_chown_single_file(tmp_path, monkeypatch):
    # Create a temporary file
    file_path = tmp_path / "testfile.txt"
    file_path.write_text("content")

    # Record calls to os.chown
    calls = []

    def fake_chown(path, uid, gid):
        calls.append((path, uid, gid))

    monkeypatch.setattr(os, "chown", fake_chown)

    # Call chown with default user/group (current user)
    chown(file_path)

    # Verify that os.chown was called once with the correct path
    assert len(calls) == 1
    called_path, called_uid, called_gid = calls[0]
    assert Path(called_path) == file_path
    # uid/gid should match current user/group
    current_uid = pwd.getpwnam(getpass.getuser()).pw_uid
    current_gid = grp.getgrgid(pwd.getpwnam(getpass.getuser()).pw_gid).gr_gid
    assert called_uid == current_uid
    assert called_gid == current_gid


def test_chown_glob_with_parent(tmp_path, monkeypatch):
    # Create a directory with two files
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    (dir_path / "a.txt").write_text("a")
    (dir_path / "b.txt").write_text("b")

    # Record calls to os.chown
    calls = []

    def fake_chown(path, uid, gid):
        calls.append((path, uid, gid))

    monkeypatch.setattr(os, "chown", fake_chown)

    # Use glob pattern to chown all files in subdir and include parent
    glob_pattern = normalize_path(dir_path / "*")
    chown(glob_pattern, include_parent=True)

    # Expect three calls: two files and the parent directory
    assert len(calls) == 3
    paths = {Path(p) for p, _, _ in calls}
    assert dir_path in paths
    assert dir_path / "a.txt" in paths
    assert dir_path / "b.txt" in paths


def test_chown_invalid_user_raises(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "testfile.txt"
    file_path.write_text("content")

    # Attempt to chown with a non‑existent user; should raise OSError
    with pytest.raises(OSError):
        chown(file_path, user="this_user_does_not_exist")
