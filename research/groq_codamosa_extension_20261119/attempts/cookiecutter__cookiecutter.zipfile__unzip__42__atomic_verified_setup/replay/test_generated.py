import os
import zipfile
import tempfile
import pytest
from pathlib import Path
from cookiecutter.zipfile import unzip
from cookiecutter.exceptions import InvalidZipRepository

def test_unzip_local_zip_with_top_level(tmp_path):
    # Create a zip file with a top‑level directory and a file inside
    top_dir = "project"
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(f"{top_dir}/", "")  # directory entry
        zf.writestr(f"{top_dir}/README.md", "# README")

    # Unzip the archive
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    # The result should be a path inside a temporary directory
    assert result.startswith(tempfile.gettempdir())
    assert Path(result).name == top_dir
    # The extracted file should exist
    extracted_file = Path(result) / "README.md"
    assert extracted_file.is_file()
    assert extracted_file.read_text() == "# README"

def test_unzip_empty_zip_raises(tmp_path):
    # Create an empty zip file
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        pass  # no entries

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    assert "empty" in str(excinfo.value).lower()

def test_unzip_missing_top_level_dir_raises(tmp_path):
    # Create a zip file that does not start with a directory entry
    zip_path = tmp_path / "bad.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("file.txt", "content")

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    assert "top-level directory" in str(excinfo.value).lower()
