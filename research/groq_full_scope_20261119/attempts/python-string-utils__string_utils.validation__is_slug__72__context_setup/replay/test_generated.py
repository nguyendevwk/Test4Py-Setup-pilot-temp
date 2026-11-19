import pytest
from string_utils.validation import is_slug

def test_is_slug_valid_slug():
    """A correctly formatted slug should return True."""
    slug = "my-blog-post-123"
    assert is_slug(slug) is True

def test_is_slug_boundary_cases():
    """Boundary inputs such as empty string, whitespace, or None should return False."""
    assert is_slug("") is False
    assert is_slug("   ") is False
    assert is_slug(None) is False

def test_is_slug_invalid_inputs():
    """Non-string inputs should be treated as invalid and return False."""
    assert is_slug(123) is False
    assert is_slug(3.14) is False
    assert is_slug(['a', 'b']) is False
