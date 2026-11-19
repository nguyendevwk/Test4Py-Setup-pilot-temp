import pytest
from string_utils.validation import is_slug


def test_is_slug_valid_basic():
    """A simple slug composed of lowercase letters, digits and the default separator."""
    slug = "my-blog-post-title-123"
    assert is_slug(slug) is True


def test_is_slug_invalid_non_string_and_custom_separator():
    """Non‑string input and a slug that uses a non‑default separator should be rejected."""
    # Non‑string input
    assert is_slug(42) is False
    # Using a custom separator that is not present in the string
    assert is_slug("my_blog_post_title", separator="_") is False
    # Using the custom separator correctly
    assert is_slug("my_blog_post_title", separator="_") is True


def test_is_slug_boundary_empty_and_none():
    """Edge cases: empty string and None should not be considered valid slugs."""
    assert is_slug("") is False
    assert is_slug(None) is False
