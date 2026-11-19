import re
import pytest
from string_utils.validation import is_slug

def test_is_slug_valid_slug():
    """A correctly formatted slug should return True."""
    slug = "my-blog-post-title"
    assert is_slug(slug) is True
    # Using a different separator should still work
    assert is_slug("my_blog_post_title", separator="_") is True

def test_is_slug_invalid_due_to_uppercase_or_spaces():
    """Slugs containing uppercase letters or spaces should return False."""
    # Uppercase letter
    assert is_slug("My-blog-post") is False
    # Space inside
    assert is_slug("my blog post") is False
    # Leading/trailing separator
    assert is_slug("-my-blog") is False
    assert is_slug("my-blog-") is False

def test_is_slug_non_string_input():
    """Non-string inputs should be rejected and return False."""
    assert is_slug(123) is False
    assert is_slug(None) is False
    assert is_slug(['my', 'blog']) is False
