import os
import zipfile
import tempfile
from pathlib import Path

import pytest

from cookiecutter.zipfile import unzip
from cookiecutter.exceptions import InvalidZipRepository


def test_unzip_local_zip_success(tmp_path):
    """Unzip a valid local zip containing a top‑level directory."""
    # Create a temporary directory to hold the zip
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a zip file with a top‑level directory and a file inside
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("project_dir/", "")  # directory entry
        zf.writestr("project_dir/README.md", "# Test")
    # Call unzip
    result = unzip(str(zip_path), is_url=False, clone_to_dir=repo_dir)
    # Verify that the extracted directory exists and contains the file
    extracted_dir = Path(result)
    assert extracted_dir.is_dir()
    assert (extracted_dir / "README.md").read_text() == "# Test"
    # Ensure the extracted directory name matches the top‑level directory
    assert extracted_dir.name == "project_dir"


def test_unzip_empty_zip_raises(tmp_path):
    """Unzip should raise InvalidZipRepository when the zip is empty."""
    # Create an empty zip file
    empty_zip = tmp_path / "empty.zip"
    empty_zip.touch()
    with zipfile.ZipFile(empty_zip, "w") as zf:
        pass  # no entries
    # Attempt to unzip and expect an exception
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(empty_zip), is_url=False, clone_to_dir=tmp_path)
    assert "empty" in str(excinfo.value).lower()


def test_unzip_missing_top_level_dir_raises(tmp_path):
    """Unzip should raise InvalidZipRepository when the zip lacks a top‑level directory."""
    # Create a zip file with a file at the root (no top‑level directory)
    bad_zip = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("README.md", "# No dir")
    # Attempt to unzip and expect an exception
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(bad_zip), is_url=False, clone_to_dir=tmp_path)
    assert "top-level directory" in str(excinfo.value).lower()
