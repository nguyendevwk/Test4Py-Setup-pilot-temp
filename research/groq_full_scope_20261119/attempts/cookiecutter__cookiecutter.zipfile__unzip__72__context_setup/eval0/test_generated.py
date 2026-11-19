import os
import zipfile
import pytest
from pathlib import Path
from cookiecutter.zipfile import unzip, InvalidZipRepository


def test_unzip_local_zip(tmp_path: Path) -> None:
    """Unzip a valid local zip file containing a top‑level directory."""
    # Create a simple zip file with a top‑level directory and one file
    archive_dir = tmp_path / "myproj"
    archive_dir.mkdir()
    (archive_dir / "README.md").write_text("# Test")
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for file in archive_dir.rglob("*"):
            zf.write(file, arcname=str(file.relative_to(tmp_path)))

    # Call unzip on the local file
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path, no_input=True)

    # The returned path should exist and contain the extracted files
    assert Path(result).exists()
    assert (Path(result) / "README.md").read_text() == "# Test"


def test_unzip_empty_zip_raises(tmp_path: Path) -> None:
    """Unzipping an empty zip file should raise InvalidZipRepository."""
    empty_zip = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_zip, "w") as zf:
        pass  # create an empty archive

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(empty_zip), is_url=False, clone_to_dir=tmp_path, no_input=True)

    assert "empty" in str(excinfo.value)


def test_unzip_missing_top_level_dir_raises(tmp_path: Path) -> None:
    """Unzipping a zip that does not start with a top‑level directory should raise."""
    bad_zip = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("file.txt", "content")  # file at root, no directory

    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(bad_zip), is_url=False, clone_to_dir=tmp_path, no_input=True)

    assert "top-level directory" in str(excinfo.value)
