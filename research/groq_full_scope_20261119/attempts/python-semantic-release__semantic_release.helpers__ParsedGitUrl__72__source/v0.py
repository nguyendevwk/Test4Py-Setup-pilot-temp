import pytest
from semantic_release.helpers import ParsedGitUrl

def test_parsed_git_url_creation_and_access():
    """Verify that ParsedGitUrl stores and exposes its fields correctly."""
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
    # NamedTuple should be hashable and usable as dict key
    d = {url: "value"}
    assert d[url] == "value"

def test_parsed_git_url_tuple_behavior():
    """Ensure ParsedGitUrl behaves like a tuple and supports unpacking."""
    url = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "project")
    # Unpacking
    scheme, netloc, namespace, repo_name = url
    assert scheme == "ssh"
    assert netloc == "gitlab.com"
    assert namespace == "group/subgroup"
    assert repo_name == "project"
    # Length and indexing
    assert len(url) == 4
    assert url[0] == "ssh"
    assert url[3] == "project"

def test_parsed_git_url_immutability_and_equality():
    """Check that ParsedGitUrl instances are immutable and compare correctly."""
    url1 = ParsedGitUrl("https", "example.com", "user", "repo")
    url2 = ParsedGitUrl("https", "example.com", "user", "repo")
    url3 = ParsedGitUrl("https", "example.com", "user", "other")
    # Equality
    assert url1 == url2
    assert url1 != url3
    # Immutability: attempting to modify should raise AttributeError
    with pytest.raises(AttributeError):
        url1.scheme = "http"
    with pytest.raises(AttributeError):
        url1._replace(scheme="http")  # _replace returns new instance, not modify
