import os
import zipfile
import tempfile
from pathlib import Path

import pytest

from cookiecutter.zipfile import unzip, InvalidZipRepository


def create_zip_with_dir(tmp_path: Path, dir_name: str, file_name: str, content: bytes):
    """Create a zip file containing a single file inside a top‑level directory."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(f"{dir_name}/", "")  # directory entry
        zf.writestr(f"{dir_name}/{file_name}", content)
    return zip_path


def create_empty_zip(tmp_path: Path):
    """Create an empty zip file."""
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        pass
    return zip_path


def create_bad_zip(tmp_path: Path):
    """Create a file that is not a valid zip archive."""
    bad_path = tmp_path / "bad.txt"
    bad_path.write_text("not a zip")
    return bad_path


def test_unzip_local_zip(tmp_path: Path):
    """Unzipping a valid local zip creates the expected directory structure."""
    zip_path = create_zip_with_dir(tmp_path, "project", "README.md", b"Hello")
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    # The result should be a path inside a temporary directory
    assert Path(result).is_dir()
    # The extracted directory should match the top‑level directory name
    assert Path(result).name == "project"
    # The file inside should exist and contain the correct content
    extracted_file = Path(result) / "README.md"
    assert extracted_file.read_bytes() == b"Hello"


def test_unzip_empty_zip_raises(tmp_path: Path):
    """Unzipping an empty zip raises InvalidZipRepository."""
    zip_path = create_empty_zip(tmp_path)
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    assert "empty" in str(excinfo.value).lower()


def test_unzip_bad_zip_raises(tmp_path: Path):
    """Unzipping a non‑zip file raises InvalidZipRepository."""
    bad_path = create_bad_zip(tmp_path)
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(bad_path), is_url=False, clone_to_dir=tmp_path)
    assert "not a valid zip" in str(excinfo.value).lower()
