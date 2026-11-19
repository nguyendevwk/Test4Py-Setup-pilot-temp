import os
import pwd
import grp
import pytest
from pathlib import Path
from flutils.pathutils import chown, normalize_path

# Helper to create a temporary file or directory
def _create_path(tmp_path, name, is_dir=False):
    p = tmp_path / name
    if is_dir:
        p.mkdir()
    else:
        p.write_text("test")
    return p

def test_chown_noop_when_path_missing(tmp_path, monkeypatch):
    """If the path does not exist, chown should do nothing and not raise."""
    missing = tmp_path / "nonexistent.txt"
    called = {"count": 0}

    def fake_chown(path, uid, gid):
        called["count"] += 1

    monkeypatch.setattr(os, "chown", fake_chown)
    # Ensure path does not exist
    assert not missing.exists()
    # Call chown; should not call os.chown
    chown(missing, user=str(pwd.getpwuid(os.getuid()).pw_name))
    assert called["count"] == 0

def test_chown_single_file(monkeypatch, tmp_path):
    """Chown should call os.chown once for an existing file."""
    file_path = _create_path(tmp_path, "file.txt")
    uid = pwd.getpwuid(os.getuid()).pw_uid
    gid = grp.getgrgid(os.getgid()).gr_gid
    called = {"count": 0, "uid": None, "gid": None, "path": None}

    def fake_chown(path, uid_arg, gid_arg):
        called["count"] += 1
        called["uid"] = uid_arg
        called["gid"] = gid_arg
        called["path"] = Path(path)

    monkeypatch.setattr(os, "chown", fake_chown)
    chown(file_path, user=str(pwd.getpwuid(os.getuid()).pw_name),
          group=str(grp.getgrgid(os.getgid()).gr_name))
    assert called["count"] == 1
    assert called["uid"] == uid
    assert called["gid"] == gid
    assert called["path"] == file_path.resolve()

def test_chown_glob_with_parent(tmp_path, monkeypatch):
    """When a glob pattern matches multiple files, chown should be called for each
    and optionally for the parent directory when include_parent is True."""
    dir_path = _create_path(tmp_path, "dir", is_dir=True)
    file1 = _create_path(dir_path, "a.txt")
    file2 = _create_path(dir_path, "b.txt")
    uid = pwd.getpwuid(os.getuid()).pw_uid
    gid = grp.getgrgid(os.getgid()).gr_gid
    calls = []

    def fake_chown(path, uid_arg, gid_arg):
        calls.append((Path(path).resolve(), uid_arg, gid_arg))

    monkeypatch.setattr(os, "chown", fake_chown)
    # Use glob pattern to match all files in dir
    glob_path = normalize_path(dir_path / "*")
    chown(glob_path, user=str(pwd.getpwuid(os.getuid()).pw_name),
          group=str(grp.getgrgid(os.getgid()).gr_name),
          include_parent=True)
    # Expect two file calls and one parent call
    expected_paths = {file1.resolve(), file2.resolve(), dir_path.resolve()}
    actual_paths = {call[0] for call in calls}
    assert expected_paths == actual_paths
    for _, uid_arg, gid_arg in calls:
        assert uid_arg == uid
        assert gid_arg == gid
