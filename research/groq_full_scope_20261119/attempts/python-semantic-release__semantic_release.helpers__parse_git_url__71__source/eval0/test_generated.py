import os
import sys
import pytest
from pathlib import Path
from semantic_release.helpers import parse_git_url

# Helper to construct a Windows path string for testing
def windows_path(tmp_path):
    return str(tmp_path / "repo.git")

# Test normal parsing of a standard HTTPS URL
def test_parse_https_url():
    url = "https://github.com/owner/project.git"
    result = parse_git_url(url)
    assert result.scheme == "https"
    assert result.netloc == "github.com"
    assert result.namespace == "owner"
    assert result.repo_name == "project"

# Test boundary case: implicit file URL on POSIX system
def test_parse_posix_file_url(tmp_path):
    file_path = tmp_path / "myrepo.git"
    file_path.touch()
    url = str(file_path)
    result = parse_git_url(url)
    assert result.scheme == "file"
    # On POSIX, netloc should be empty
    assert result.netloc == ""
    assert result.namespace == ""
    assert result.repo_name == "myrepo"

# Test error case: malformed URL missing scheme
def test_parse_invalid_url():
    with pytest.raises(ValueError):
        parse_git_url("not_a_valid_url")
