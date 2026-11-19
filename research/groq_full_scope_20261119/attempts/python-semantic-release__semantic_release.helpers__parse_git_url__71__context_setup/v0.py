import os
import sys
import pytest
from pathlib import Path
from semantic_release.helpers import parse_git_url, ParsedGitUrl

def test_parse_http_and_https_urls():
    # Normal HTTP/HTTPS URLs should be parsed correctly
    url = "https://github.com/owner/repo.git"
    result = parse_git_url(url)
    assert isinstance(result, ParsedGitUrl)
    assert result.scheme == "https"
    assert result.netloc == "github.com"
    assert result.namespace == "owner"
    assert result.repo_name == "repo"

    # URL without .git suffix should still work
    url_no_git = "http://git.mycompany.com/username/myproject"
    result_no_git = parse_git_url(url_no_git)
    assert result_no_git.scheme == "http"
    assert result_no_git.netloc == "git.mycompany.com"
    assert result_no_git.namespace == "username"
    assert result_no_git.repo_name == "myproject"

def test_parse_file_and_windows_paths(tmp_path: Path):
    # Posix file path
    posix_path = tmp_path / "repo.git"
    posix_path.touch()
    posix_url = f"file://{posix_path}"
    result_posix = parse_git_url(posix_url)
    assert result_posix.scheme == "file"
    assert result_posix.netloc == ""
    assert result_posix.namespace == ""
    assert result_posix.repo_name == "repo"

    # Windows file path (simulate by using a drive letter)
    if sys.platform.startswith("win"):
        win_path = Path(f"C:/Users/Dev/{posix_path.name}")
        win_path.touch()
        win_url = f"file:///{win_path}"
        result_win = parse_git_url(win_url)
        assert result_win.scheme == "file"
        assert result_win.netloc == ""
        assert result_win.namespace == ""
        assert result_win.repo_name == "repo"
    else:
        # On non‑Windows platforms we skip the Windows‑specific check
        pytest.skip("Windows path test only applicable on Windows")

def test_parse_invalid_and_boundary_urls():
    # URL missing scheme should raise ValueError
    with pytest.raises(ValueError, match="Cannot parse"):
        parse_git_url("git@github.com:owner/repo.git")

    # URL with empty netloc for non‑file scheme should raise ValueError
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("ssh:///owner/repo.git")

    # URL with missing namespace should raise ValueError
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https://github.com/.git")

    # URL with missing repo name should raise ValueError
    with pytest.raises(ValueError, match="Bad url"):
        parse_git_url("https://github.com/owner/")

    # URL with unsupported scheme should still parse but not raise
    # (the function does not validate scheme, only checks presence)
    result = parse_git_url("custom://host/owner/repo.git")
    assert result.scheme == "custom"
    assert result.netloc == "host"
    assert result.namespace == "owner"
    assert result.repo_name == "repo"
