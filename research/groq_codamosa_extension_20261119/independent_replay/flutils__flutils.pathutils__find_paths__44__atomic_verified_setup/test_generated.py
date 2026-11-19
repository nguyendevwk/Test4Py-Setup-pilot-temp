import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths


def test_find_paths_with_glob(tmp_path):
    """Normal case: pattern matches multiple files and directories."""
    # Create a directory structure
    (tmp_path / "file_one").write_text("content")
    (tmp_path / "dir_one").mkdir()
    (tmp_path / "dir_one" / "inner.txt").write_text("inner")
    # Pattern that matches everything in tmp_path
    pattern = str(tmp_path / "*")
    # Collect results
    results = list(find_paths(pattern))
    # Expect both the file and the directory to be returned
    expected = {tmp_path / "file_one", tmp_path / "dir_one"}
    assert set(results) == expected
    # Ensure that the inner file is not returned by the top-level glob
    assert all(p.name != "inner.txt" for p in results)


def test_find_paths_no_matches(tmp_path):
    """Boundary case: pattern matches nothing."""
    # Ensure tmp_path is empty
    assert not any(tmp_path.iterdir())
    # Pattern that cannot match any file
    pattern = str(tmp_path / "nonexistent_*")
    results = list(find_paths(pattern))
    # Expect an empty list
    assert results == []


def test_find_paths_bytes_pattern(tmp_path):
    """Error/edge case: pattern provided as bytes."""
    # Create a file to match
    (tmp_path / "sample.txt").write_text("data")
    # Use bytes pattern
    pattern = (tmp_path / "sample.txt").as_posix().encode()
    # find_paths should accept bytes and yield the file
    results = list(find_paths(pattern))
    assert results == [tmp_path / "sample.txt"]
