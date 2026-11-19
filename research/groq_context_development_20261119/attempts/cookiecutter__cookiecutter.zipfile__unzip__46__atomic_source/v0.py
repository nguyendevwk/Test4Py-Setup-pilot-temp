import os
import zipfile
import tempfile
from pathlib import Path

import pytest

from cookiecutter.zipfile import unzip
from cookiecutter.exceptions import InvalidZipRepository


def test_unzip_local_zip_with_top_level(tmp_path):
    """Unzipping a valid local zip containing a top‑level directory succeeds."""
    # Create a temporary zip file with a top‑level directory and a file inside
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("myproject/", "")  # directory entry
        zf.writestr("myproject/README.md", "# Test")

    # Call unzip on the local file
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    # The returned path should point to the extracted directory
    extracted_dir = Path(result)
    assert extracted_dir.is_dir()
    assert extracted_dir.name == "myproject"
    assert (extracted_dir / "README.md").read_text() == "# Test"


def test_unzip_empty_zip_raises(tmp_path):
    """An empty zip file triggers InvalidZipRepository."""
    zip_path = tmp_path / "empty.zip"
    # Create an empty zip file
    with zipfile.ZipFile(zip_path, "w") as zf:
        pass

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    assert "empty" in str(excinfo.value).lower()


def test_unzip_zip_without_top_level_dir_raises(tmp_path):
    """A zip that does not start with a top‑level directory raises an error."""
    zip_path = tmp_path / "no_dir.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("file.txt", "content")  # no directory entry

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    assert "top-level directory" in str(excinfo.value).lower()
