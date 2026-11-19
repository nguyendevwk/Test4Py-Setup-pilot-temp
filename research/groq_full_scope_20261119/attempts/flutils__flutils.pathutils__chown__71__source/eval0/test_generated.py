import os
import pwd
import grp
import pytest
from pathlib import Path
from flutils.pathutils import chown, normalize_path

# Helper to create a temporary file or directory
def create_path(tmp_path, name, is_dir=False):
    p = tmp_path / name
    if is_dir:
        p.mkdir()
    else:
        p.write_text("test")
    return p

def test_chown_noop_when_path_missing(tmp_path, monkeypatch):
    # Ensure chown does nothing when the path does not exist
    missing = tmp_path / "nonexistent.txt"
    called = {"count": 0}
    def fake_chown(path, uid, gid):
        called["count"] += 1
    monkeypatch.setattr(os, "chown", fake_chown)

    chown(missing)
    assert called["count"] == 0, "os.chown should not be called for missing path"

def test_chown_changes_owner_and_group(tmp_path, monkeypatch):
    # Create a file and verify that os.chown is called with correct uid/gid
    file_path = create_path(tmp_path, "file.txt")
    uid = pwd.getpwnam(os.getlogin()).pw_uid
    gid = grp.getgrgid(os.getgid()).gr_gid
    called = {"uid": None, "gid": None}
    def fake_chown(path, uid_arg, gid_arg):
        called["uid"] = uid_arg
        called["gid"] = gid_arg
    monkeypatch.setattr(os, "chown", fake_chown)

    chown(file_path, user=os.getlogin(), group=os.getgid())
    assert called["uid"] == uid, f"Expected uid {uid}, got {called['uid']}"
    assert called["gid"] == gid, f"Expected gid {gid}, got {called['gid']}"

def test_chown_with_glob_and_include_parent(tmp_path, monkeypatch):
    # Create a directory with two files and test glob pattern with include_parent
    dir_path = create_path(tmp_path, "dir", is_dir=True)
    file1 = create_path(dir_path, "a.txt")
    file2 = create_path(dir_path, "b.txt")
    uid = pwd.getpwnam(os.getlogin()).pw_uid
    gid = grp.getgrgid(os.getgid()).gr_gid
    called = {"paths": []}
    def fake_chown(path, uid_arg, gid_arg):
        called["paths"].append((path, uid_arg, gid_arg))
    monkeypatch.setattr(os, "chown", fake_chown)

    # Use glob pattern to match all files in dir and include parent
    chown(f"{dir_path.as_posix()}/**", user=os.getlogin(), group=os.getgid(), include_parent=True)

    # Expect chown called for each file and for the parent directory
    expected_paths = {file1.as_posix(), file2.as_posix(), dir_path.as_posix()}
    actual_paths = {p[0] for p in called["paths"]}
    assert expected_paths == actual_paths, f"Expected paths {expected_paths}, got {actual_paths}"
    for _, uid_arg, gid_arg in called["paths"]:
        assert uid_arg == uid, f"Expected uid {uid}, got {uid_arg}"
        assert gid_arg == gid, f"Expected gid {gid}, got {gid_arg}"
