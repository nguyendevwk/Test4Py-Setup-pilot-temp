import os
import zipfile
import pytest
from pathlib import Path
from cookiecutter.zipfile import unzip
from cookiecutter.exceptions import InvalidZipRepository

def test_unzip_local_zip(tmp_path):
    # Create a simple zip file with a top‑level directory
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "file.txt").write_text("content")
    zip_path = tmp_path / "repo.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(repo_dir / "file.txt", arcname="repo/file.txt")
    # Unzip
    result = unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path, no_input=True)
    # Verify the extracted directory exists and contains the file
    extracted = Path(result)
    assert extracted.is_dir()
    assert (extracted / "file.txt").read_text() == "content"

def test_unzip_empty_zip_raises(tmp_path):
    # Create an empty zip file
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        pass
    # Unzip should raise InvalidZipRepository
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path, no_input=True)
    assert "empty" in str(excinfo.value)

def test_unzip_password_protected_no_input_raises(tmp_path):
    # Create a password‑protected zip file
    zip_path = tmp_path / "protected.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("protected/file.txt", b"secret", compress_type=zipfile.ZIP_DEFLATED, pwd=b"mypwd")
    # Unzip with no_input=True should raise InvalidZipRepository
    with pytest.raises(InvalidZipRepository) as excinfo:
        unzip(str(zip_path), is_url=False, clone_to_dir=tmp_path, no_input=True)
    assert "Unable to unlock password protected repository" in str(excinfo.value)
