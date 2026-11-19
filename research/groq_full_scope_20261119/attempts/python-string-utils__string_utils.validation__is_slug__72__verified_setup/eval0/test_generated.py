import pytest
from string_utils.validation import is_slug

def test_is_slug_valid_and_invalid():
    # Valid slug: lowercase letters, digits, and separator
    assert is_slug("my-blog-post-123") is True
    # Invalid slug: contains uppercase letter
    assert is_slug("My-blog-post") is False
    # Invalid slug: starts with separator
    assert is_slug("-my-blog") is False
    # Invalid slug: ends with separator
    assert is_slug("my-blog-") is False
    # Invalid slug: contains consecutive separators
    assert is_slug("my--blog") is False

def test_is_slug_with_custom_separator():
    # Using underscore as separator
    assert is_slug("my_blog_post", separator="_") is True
    # Invalid with default separator but underscore present
    assert is_slug("my_blog_post") is False
    # Valid with mixed separators but only underscore allowed
    assert is_slug("my_blog_post", separator="_") is True
    # Invalid: contains default separator when custom separator is used
    assert is_slug("my-blog_post", separator="_") is False

def test_is_slug_non_string_input():
    # Non-string input should return False, not raise
    assert is_slug(12345) is False
    assert is_slug(None) is False
    assert is_slug(["my", "blog"]) is False
