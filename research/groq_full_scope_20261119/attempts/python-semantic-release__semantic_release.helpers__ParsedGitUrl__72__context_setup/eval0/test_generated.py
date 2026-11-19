import pytest
from semantic_release.helpers import ParsedGitUrl

def test_parsed_git_url_creation_and_access():
    """Verify that a ParsedGitUrl instance stores and exposes its fields correctly."""
    url = ParsedGitUrl(scheme="https", netloc="github.com", namespace="org", repo_name="repo")
    assert url.scheme == "https"
    assert url.netloc == "github.com"
    assert url.namespace == "org"
    assert url.repo_name == "repo"
    # Ensure the tuple representation matches the expected order
    assert tuple(url) == ("https", "github.com", "org", "repo")

def test_parsed_git_url_unpacking_and_equality():
    """Test unpacking into variables and equality comparison."""
    url1 = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "project")
    scheme, netloc, namespace, repo_name = url1
    assert scheme == "ssh"
    assert netloc == "gitlab.com"
    assert namespace == "group/subgroup"
    assert repo_name == "project"

    url2 = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "project")
    assert url1 == url2  # NamedTuple equality compares all fields
    # Different field should cause inequality
    url3 = ParsedGitUrl("ssh", "gitlab.com", "group/subgroup", "different")
    assert url1 != url3

def test_parsed_git_url_immutability_and_hashability():
    """Ensure that ParsedGitUrl instances are immutable and hashable."""
    url = ParsedGitUrl("https", "example.com", "user", "repo")
    with pytest.raises(TypeError):
        # Attempt to modify an attribute should raise
        url.scheme = "http"
    # NamedTuple instances are hashable; use in a set
    url_set = {url}
    assert url in url_set
    # Hash value should be consistent across identical instances
    url_duplicate = ParsedGitUrl("https", "example.com", "user", "repo")
    assert hash(url) == hash(url_duplicate)
