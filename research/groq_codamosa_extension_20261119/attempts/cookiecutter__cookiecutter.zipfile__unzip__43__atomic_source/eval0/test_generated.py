import os
import zipfile
import tempfile
from pathlib import Path

import pytest

from cookiecutter.zipfile import unzip, InvalidZipRepository


def create_zip_with_contents(zip_path: Path, entries: list[tuple[str, bytes]]):
    """Create a zip file at zip_path containing the given entries."""
    with zipfile.ZipFile(zip_path, "w") as zf:
        for name, data in entries:
            zf.writestr(name, data)


def test_unzip_local_zip_success(tmp_path: Path):
    """Unzipping a valid local zip file creates the expected directory."""
    # Create a zip with a top‑level directory and a file inside it
    zip_path = tmp_path / "test.zip"
    create_zip_with_contents(
        zip_path,
        [("project/", b""), ("project/README.md", b"# Test")],
    )

    # Unzip into a temporary directory
    result_path = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    # The result should be a path to the extracted project directory
    assert Path(result_path).exists()
    assert Path(result_path).is_dir()
    assert (Path(result_path) / "README.md").read_text() == "# Test"


def test_unzip_empty_zip_raises(tmp_path: Path):
    """Unzipping an empty zip file raises InvalidZipRepository."""
    # Create an empty zip file
    zip_path = tmp_path / "empty.zip"
    zip_path.touch()  # zero‑length file

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    assert "empty" in str(excinfo.value).lower()


def test_unzip_missing_top_level_directory_raises(tmp_path: Path):
    """Unzipping a zip that does not start with a directory entry raises."""
    # Create a zip with a single file, no top‑level directory
    zip_path = tmp_path / "nofolder.zip"
    create_zip_with_contents(zip_path, [("file.txt", b"content")])

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    assert "top-level directory" in str(excinfo.value).lower()
