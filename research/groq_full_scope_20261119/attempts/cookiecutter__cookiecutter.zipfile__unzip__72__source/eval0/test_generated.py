import os
import zipfile
import tempfile
from pathlib import Path

import pytest

from cookiecutter.zipfile import unzip
from cookiecutter.exceptions import InvalidZipRepository


def test_unzip_local_zip_with_top_level(tmp_path):
    """Unzip a valid local zip containing a top‑level directory."""
    # Create a zip file with a top‑level directory and a file inside
    top_dir = "project"
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(f"{top_dir}/", "")  # directory entry
        zf.writestr(f"{top_dir}/README.md", "# Test")

    # Call unzip on the local file
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    # The returned path should point to the extracted directory
    extracted = Path(result)
    assert extracted.is_dir()
    assert (extracted / "README.md").read_text() == "# Test"
    # The temporary extraction directory should be inside a temp dir
    assert extracted.parent.name.startswith("tmp")


def test_unzip_empty_zip_raises(tmp_path):
    """Unzip should raise InvalidZipRepository for an empty zip file."""
    empty_zip = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_zip, "w") as zf:
        pass  # no entries

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(empty_zip), is_url=False, clone_to_dir=tmp_path)

    assert "empty" in str(excinfo.value).lower()


def test_unzip_missing_top_level_directory_raises(tmp_path):
    """Unzip should raise InvalidZipRepository if the first entry is not a directory."""
    bad_zip = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("file.txt", "content")  # no top‑level directory

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(bad_zip), is_url=False, clone_to_dir=tmp_path)

    assert "top-level directory" in str(excinfo.value).lower()
