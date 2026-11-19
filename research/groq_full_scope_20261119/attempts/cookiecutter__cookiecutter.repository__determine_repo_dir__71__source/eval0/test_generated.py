import os
import json
import zipfile
import tempfile
import shutil
from pathlib import Path

import pytest

from cookiecutter.repository import determine_repo_dir, RepositoryNotFound


def _create_cookiecutter_dir(base: Path) -> Path:
    """Create a directory containing a minimal cookiecutter.json."""
    dir_path = base / "template"
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "cookiecutter.json").write_text(json.dumps({"project_name": "demo"}))
    return dir_path


def _create_zip_with_cookiecutter(tmp_path: Path) -> Path:
    """Create a zip file containing a cookiecutter.json."""
    zip_path = tmp_path / "template.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("cookiecutter.json", json.dumps({"project_name": "demo"}))
    return zip_path


def test_determine_repo_dir_local_path(tmp_path: Path):
    """When template is a local path, the function returns that path."""
    template_dir = _create_cookiecutter_dir(tmp_path)
    clone_to_dir = tmp_path / "clone"
    clone_to_dir.mkdir()
    result_dir, cleanup = determine_repo_dir(
        template=str(template_dir),
        abbreviations={},
        clone_to_dir=clone_to_dir,
        checkout=None,
        no_input=True,
    )
    assert result_dir == str(template_dir)
    assert cleanup is False
    # The directory should still exist after the call
    assert Path(result_dir).exists()


def test_determine_repo_dir_zip_file(tmp_path: Path):
    """When template is a zip file, it is unzipped and returned."""
    zip_path = _create_zip_with_cookiecutter(tmp_path)
    clone_to_dir = tmp_path / "clone"
    clone_to_dir.mkdir()
    result_dir, cleanup = determine_repo_dir(
        template=str(zip_path),
        abbreviations={},
        clone_to_dir=clone_to_dir,
        checkout=None,
        no_input=True,
    )
    # The unzipped directory should be inside clone_to_dir
    assert Path(result_dir).is_dir()
    assert Path(result_dir).joinpath("cookiecutter.json").exists()
    assert cleanup is True
    # After cleanup flag is True, the directory should be removed by caller
    # (here we just check that it exists now)
    assert Path(result_dir).exists()


def test_determine_repo_dir_missing(tmp_path: Path):
    """If no cookiecutter.json is found, a RepositoryNotFound is raised."""
    missing_dir = tmp_path / "missing"
    missing_dir.mkdir()
    clone_to_dir = tmp_path / "clone"
    clone_to_dir.mkdir()
    with pytest.raises(RepositoryNotFound) as excinfo:
        determine_repo_dir(
            template=str(missing_dir),
            abbreviations={},
            clone_to_dir=clone_to_dir,
            checkout=None,
            no_input=True,
        )
    assert str(missing_dir) in str(excinfo.value)
