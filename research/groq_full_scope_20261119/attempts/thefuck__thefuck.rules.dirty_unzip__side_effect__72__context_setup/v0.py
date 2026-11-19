import os
import zipfile
import tempfile
import shutil
import pathlib

from thefuck.rules.dirty_unzip import side_effect, _zip_file


class DummyCommand:
    def __init__(self, script_parts):
        self.script_parts = script_parts


def create_zip(zip_path, files):
    """Create a zip file containing the given files mapping name->content."""
    with zipfile.ZipFile(zip_path, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)


def test_side_effect_removes_files_in_cwd(tmp_path):
    """Files listed in the zip that are inside the current working directory are removed."""
    cwd = tmp_path
    os.chdir(cwd)

    # Create a file that will be removed
    target_file = cwd / "to_remove.txt"
    target_file.write_text("remove me")

    # Create a zip containing that file
    zip_path = cwd / "archive.zip"
    create_zip(zip_path, {"to_remove.txt": "content"})

    # Run side_effect
    cmd = DummyCommand(["unzip", str(zip_path)])
    side_effect(cmd, None)

    # Assert the file has been removed
    assert not target_file.exists()


def test_side_effect_skips_files_outside_cwd(tmp_path, tmp_path_factory):
    """Files listed in the zip that are outside the current working directory are not removed."""
    cwd = tmp_path
    os.chdir(cwd)

    # Create a file outside cwd
    outside_dir = tmp_path_factory.mktemp("outside")
    outside_file = outside_dir / "outside.txt"
    outside_file.write_text("do not remove")

    # Create a zip containing the absolute path of the outside file
    zip_path = cwd / "archive.zip"
    create_zip(zip_path, {str(outside_file): "content"})

    # Run side_effect
    cmd = DummyCommand(["unzip", str(zip_path)])
    side_effect(cmd, None)

    # Assert the outside file still exists
    assert outside_file.exists()


def test_side_effect_ignores_directories(tmp_path):
    """Directories inside the zip are not removed; only files are attempted."""
    cwd = tmp_path
    os.chdir(cwd)

    # Create a directory that will be present after extraction
    dir_path = cwd / "dir"
    dir_path.mkdir()

    # Create a zip containing a file and a directory entry
    zip_path = cwd / "archive.zip"
    create_zip(zip_path, {"dir/": "", "dir/file.txt": "content"})

    # Create the file inside the directory to simulate extraction
    file_path = dir_path / "file.txt"
    file_path.write_text("content")

    # Run side_effect
    cmd = DummyCommand(["unzip", str(zip_path)])
    side_effect(cmd, None)

    # The file should be removed
    assert not file_path.exists()
    # The directory should still exist
    assert dir_path.is_dir()
