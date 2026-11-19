import os
import zipfile
import tempfile
import pytest
from pathlib import Path
from cookiecutter.zipfile import unzip, InvalidZipRepository


def test_unzip_local_zip(tmp_path):
    """Unzipping a valid local zip creates the expected directory."""
    # Create a simple zip file with a top‑level directory
    archive_dir = tmp_path / "myproj"
    archive_dir.mkdir()
    (archive_dir / "file.txt").write_text("hello")
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for root, _, files in os.walk(archive_dir):
            for f in files:
                full_path = Path(root) / f
                zf.write(full_path, arcname=str(full_path.relative_to(tmp_path)))

    # Unzip
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)

    # Verify the extracted directory exists and contains the file
    extracted = Path(result)
    assert extracted.is_dir()
    assert (extracted / "file.txt").read_text() == "hello"


def test_unzip_empty_zip_raises(tmp_path):
    """Unzipping an empty zip raises InvalidZipRepository."""
    empty_zip = tmp_path / "empty.zip"
    empty_zip.write_bytes(b"")  # create an empty file
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(empty_zip), is_url=False, clone_to_dir=tmp_path)
    assert "empty" in str(excinfo.value).lower()


def test_unzip_invalid_zip_raises(tmp_path):
    """Unzipping a non‑zip file raises InvalidZipRepository."""
    not_a_zip = tmp_path / "notzip.txt"
    not_a_zip.write_text("just some text")
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(not_a_zip), is_url=False, clone_to_dir=tmp_path)
    assert "not a valid zip archive" in str(excinfo.value).lower()
