import os
import zipfile
import tempfile
import pytest
from pathlib import Path
from cookiecutter.zipfile import unzip, InvalidZipRepository


def create_zip_with_dir(tmp_path: Path, dir_name: str, file_name: str = "file.txt") -> Path:
    """Create a zip file containing a single directory with one file."""
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(f"{dir_name}/", "")  # directory entry
        zf.writestr(f"{dir_name}/{file_name}", "content")
    return zip_path


def create_empty_zip(tmp_path: Path) -> Path:
    """Create an empty zip file."""
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        pass
    return zip_path


def create_zip_without_dir(tmp_path: Path) -> Path:
    """Create a zip file that does not start with a top‑level directory."""
    zip_path = tmp_path / "nodir.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("file.txt", "content")
    return zip_path


def test_unzip_success(tmp_path: Path):
    """Unzip a valid archive containing a top‑level directory."""
    zip_path = create_zip_with_dir(tmp_path, "project")
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    # The returned path should point to the extracted directory
    assert Path(result).name == "project"
    # The extracted directory should contain the file we added
    extracted_file = Path(result) / "file.txt"
    assert extracted_file.is_file()
    assert extracted_file.read_text() == "content"


def test_unzip_empty_archive(tmp_path: Path):
    """Unzipping an empty archive should raise InvalidZipRepository."""
    zip_path = create_empty_zip(tmp_path)
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    assert "is empty" in str(excinfo.value)


def test_unzip_missing_top_level_dir(tmp_path: Path):
    """Unzipping an archive that lacks a top‑level directory should raise InvalidZipRepository."""
    zip_path = create_zip_without_dir(tmp_path)
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path)
    assert "does not include a top-level directory" in str(excinfo.value)
