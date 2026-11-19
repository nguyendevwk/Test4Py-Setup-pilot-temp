import os
import sys
import pytest
from pathlib import Path

# Import the target function and the ParsedGitUrl dataclass
from semantic_release.helpers import parse_git_url, ParsedGitUrl


def test_parse_git_url_http_and_file(tmp_path: Path):
    """Test parsing of a standard HTTPS URL and a local file path."""
    # HTTPS URL
    https_url = "https://github.com/owner/repo.git"
    result = parse_git_url(https_url)
    assert isinstance(result, ParsedGitUrl)
    assert result.scheme == "https"
    assert result.netloc == "github.com"
    assert result.namespace == "owner"
    assert result.repo_name == "repo"

    # Local file path (POSIX)
    local_path = tmp_path / "repo.git"
    local_path.touch()
    file_url = f"file://{local_path}"
    result_file = parse_git_url(file_url)
    assert result_file.scheme == "file"
    assert result_file.netloc == ""
    assert result_file.namespace == ""
    assert result_file.repo_name == "repo"


def test_parse_git_url_ssh_and_windows(tmp_path: Path):
    """Test parsing of SSH URLs and Windows file paths."""
    # SSH URL with explicit user and port
    ssh_url = "ssh://git@github.com:2222/owner/repo.git"
    result = parse_git_url(ssh_url)
    assert result.scheme == "ssh"
    assert result.netloc == "git@github.com:2222"
    assert result.namespace == "owner"
    assert result.repo_name == "repo"

    # Windows file path
    windows_path = Path("C:/Users/Me/project.git")
    windows_path.touch()
    windows_url = f"file:///{windows_path}"
    result_win = parse_git_url(windows_url)
    assert result_win.scheme == "file"
    assert result_win.netloc == ""
    assert result_win.namespace == ""
    assert result_win.repo_name == "project"


def test_parse_git_url_invalid_and_boundary():
    """Test that invalid URLs raise ValueError and boundary cases are handled."""
    # Missing scheme
    with pytest.raises(ValueError, match="Cannot parse"):
        parse_git_url("github.com/owner/repo.git")

    # Empty path after scheme
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https://github.com/")

    # URL with .git suffix missing
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https://github.com/owner/")

    # URL with unsupported scheme
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("ftp://github.com/owner/repo.git")
