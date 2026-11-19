import pytest
from semantic_release.helpers import ParsedGitUrl

def test_parsed_git_url_basic_attributes():
    """ParsedGitUrl should store and expose its components correctly."""
    url = ParsedGitUrl(
        scheme="https",
        netloc="github.com",
        namespace="org",
        repo_name="repo",
    )
    assert url.scheme == "https"
    assert url.netloc == "github.com"
    assert url.namespace == "org"
    assert url.repo_name == "repo"
    # NamedTuple should support tuple indexing
    assert url[0] == "https"
    assert url[1] == "github.com"
    assert url[2] == "org"
    assert url[3] == "repo"

def test_parsed_git_url_equality_and_hash():
    """Two ParsedGitUrl instances with the same data should be equal and hash the same."""
    a = ParsedGitUrl("ssh", "gitlab.com", "group", "project")
    b = ParsedGitUrl("ssh", "gitlab.com", "group", "project")
    c = ParsedGitUrl("ssh", "gitlab.com", "group", "different")
    assert a == b
    assert a != c
    # Hashes should match for equal instances
    assert hash(a) == hash(b)
    # Hashes should differ for non-equal instances
    assert hash(a) != hash(c)

def test_parsed_git_url_unpacking_and_repr():
    """ParsedGitUrl should unpack correctly and have a readable representation."""
    url = ParsedGitUrl("git", "bitbucket.org", "team", "repo")
    scheme, netloc, namespace, repo_name = url
    assert scheme == "git"
    assert netloc == "bitbucket.org"
    assert namespace == "team"
    assert repo_name == "repo"
    # Representation should include all fields
    rep = repr(url)
    assert "git" in rep
    assert "bitbucket.org" in rep
    assert "team" in rep
    assert "repo" in rep
