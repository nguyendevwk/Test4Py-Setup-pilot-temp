import os
import zipfile
import tempfile
from pathlib import Path

import pytest

from cookiecutter.zipfile import unzip
from cookiecutter.exceptions import InvalidZipRepository


def test_unzip_local_zip(tmp_path):
    """Unzipping a valid local zip creates the expected directory and files."""
    # Create a temporary directory with a file
    src_dir = tmp_path / "project"
    src_dir.mkdir()
    (src_dir / "README.md").write_text("# Test")

    # Zip the directory
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for file in src_dir.rglob("*"):
            zf.write(file, arcname=os.path.relpath(file, src_dir.parent))

    # Unzip
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    # Verify the extracted directory exists and contains the file
    extracted_dir = Path(result)
    assert extracted_dir.is_dir()
    assert (extracted_dir / "project" / "README.md").read_text() == "# Test"


def test_unzip_empty_zip(tmp_path):
    """Unzipping an empty zip raises InvalidZipRepository."""
    empty_zip = tmp_path / "empty.zip"
    empty_zip.write_bytes(b"")  # zero bytes, not a valid zip

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(empty_zip), is_url=False, clone_to_dir=tmp_path)

    assert "not a valid zip archive" in str(excinfo.value)


def test_unzip_missing_top_level_dir(tmp_path):
    """Unzipping a zip without a top‑level directory raises InvalidZipRepository."""
    # Create a zip that contains a file at the root, not inside a directory
    bad_zip = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("file.txt", "content")

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(bad_zip), is_url=False, clone_to_dir=tmp_path)

    assert "does not include a top-level directory" in str(excinfo.value)
