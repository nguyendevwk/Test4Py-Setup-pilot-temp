import pytest
from semantic_release.helpers import ParsedGitUrl

def test_parsed_git_url_basic_attributes():
    """Verify that the NamedTuple stores and exposes its fields correctly."""
    url = ParsedGitUrl(scheme="https", netloc="github.com", namespace="org", repo_name="repo")
    assert url.scheme == "https"
    assert url.netloc == "github.com"
    assert url.namespace == "org"
    assert url.repo_name == "repo"
    # The tuple representation should match the order of fields
    assert tuple(url) == ("https", "github.com", "org", "repo")

def test_parsed_git_url_equality_and_hash():
    """Ensure that two instances with identical data are equal and hash consistently."""
    a = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "project")
    b = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "project")
    c = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "different")
    assert a == b
    assert a != c
    # Hashes of equal objects must be equal
    assert hash(a) == hash(b)
    # Hashes of unequal objects should differ (not guaranteed but highly likely)
    assert hash(a) != hash(c)

def test_parsed_git_url_tuple_behavior():
    """Test that the NamedTuple behaves like a regular tuple."""
    url = ParsedGitUrl("git", "example.com", "user", "repo")
    # Indexing
    assert url[0] == "git"
    assert url[1] == "example.com"
    assert url[2] == "user"
    assert url[3] == "repo"
    # Slicing
    assert url[:2] == ("git", "example.com")
    assert url[2:] == ("user", "repo")
    # Iteration
    collected = [part for part in url]
    assert collected == ["git", "example.com", "user", "repo"]
