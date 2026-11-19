import pytest
from semantic_release.helpers import ParsedGitUrl

def test_parsed_git_url_creation_and_access():
    """Ensure that ParsedGitUrl correctly stores and exposes its fields."""
    url = ParsedGitUrl(scheme="https", netloc="github.com", namespace="org", repo_name="repo")
    assert url.scheme == "https"
    assert url.netloc == "github.com"
    assert url.namespace == "org"
    assert url.repo_name == "repo"
    # NamedTuple should be immutable
    with pytest.raises(AttributeError):
        url.scheme = "git"

def test_parsed_git_url_equality_and_hash():
    """ParsedGitUrl instances should compare equal when all fields match and be hashable."""
    a = ParsedGitUrl("ssh", "gitlab.com", "group", "project")
    b = ParsedGitUrl("ssh", "gitlab.com", "group", "project")
    c = ParsedGitUrl("ssh", "gitlab.com", "group", "different")
    assert a == b
    assert a != c
    # Hash consistency
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)

def test_parsed_git_url_tuple_behavior():
    """ParsedGitUrl should behave like a tuple for indexing and unpacking."""
    url = ParsedGitUrl("git", "bitbucket.org", "team", "repo")
    # Indexing
    assert url[0] == "git"
    assert url[1] == "bitbucket.org"
    assert url[2] == "team"
    assert url[3] == "repo"
    # Unpacking
    scheme, netloc, namespace, repo_name = url
    assert scheme == "git"
    assert netloc == "bitbucket.org"
    assert namespace == "team"
    assert repo_name == "repo"
    # Length
    assert len(url) == 4
