import os
import sys
import pytest
from pathlib import Path
from semantic_release.helpers import parse_git_url, ParsedGitUrl

def test_parse_git_url_http_and_file(tmp_path):
    # HTTP URL
    http_url = "https://github.com/owner/repo.git"
    parsed_http = parse_git_url(http_url)
    assert isinstance(parsed_http, ParsedGitUrl)
    assert parsed_http.scheme == "https"
    assert parsed_http.netloc == "github.com"
    assert parsed_http.namespace == "owner"
    assert parsed_http.repo_name == "repo"

    # File URL on POSIX
    file_path = tmp_path / "repo.git"
    file_url = f"file://{file_path}"
    parsed_file = parse_git_url(file_url)
    assert parsed_file.scheme == "file"
    assert parsed_file.netloc == ""
    assert parsed_file.namespace == ""
    assert parsed_file.repo_name == "repo"

    # File URL on Windows (only if running on Windows)
    if os.name == "nt":
        win_path = Path("C:\\Users\\test\\repo.git")
        win_url = f"file://{win_path}"
        parsed_win = parse_git_url(win_url)
        assert parsed_win.scheme == "file"
        assert parsed_win.netloc == ""
        assert parsed_win.namespace == ""
        assert parsed_win.repo_name == "repo"

def test_parse_git_url_ssh_and_git_scheme():
    # SSH URL with explicit ssh://
    ssh_url = "ssh://git@github.com:22/owner/repo.git"
    parsed_ssh = parse_git_url(ssh_url)
    assert parsed_ssh.scheme == "ssh"
    assert parsed_ssh.netloc == "git@github.com:22"
    assert parsed_ssh.namespace == "owner"
    assert parsed_ssh.repo_name == "repo"

    # git:// scheme
    git_url = "git://host.xz/path/to/repo.git/"
    parsed_git = parse_git_url(git_url)
    assert parsed_git.scheme == "git"
    assert parsed_git.netloc == "host.xz"
    assert parsed_git.namespace == "path/to"
    assert parsed_git.repo_name == "repo"

    # Implicit SSH (scp-like) syntax
    scp_url = "git@github.com:owner/repo.git"
    parsed_scp = parse_git_url(scp_url)
    assert parsed_scp.scheme == "ssh"
    assert parsed_scp.netloc == "git@github.com"
    assert parsed_scp.namespace == "owner"
    assert parsed_scp.repo_name == "repo"

def test_parse_git_url_errors():
    # Missing scheme
    with pytest.raises(ValueError, match="Cannot parse"):
        parse_git_url("github.com/owner/repo.git")

    # Missing netloc for non-file scheme
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https:///owner/repo.git")

    # Missing namespace
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https://github.com/.git")

    # Missing repo name
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https://github.com/owner/")
