import pytest
from string_utils.validation import is_slug

def test_is_slug_valid_and_invalid_cases():
    # Valid slug with default separator
    assert is_slug("my-blog-post-title") is True
    # Invalid because of uppercase letters
    assert is_slug("My-blog-post-title") is False
    # Invalid because of leading separator
    assert is_slug("-my-blog-post-title") is False
    # Invalid because of trailing separator
    assert is_slug("my-blog-post-title-") is False
    # Invalid because of consecutive separators
    assert is_slug("my--blog-post") is False
    # Invalid because of non-alphanumeric characters
    assert is_slug("my_blog_post") is False

def test_is_slug_with_custom_separator_and_edge_cases():
    # Valid slug with underscore separator
    assert is_slug("my_blog_post", separator="_") is True
    # Invalid because of uppercase letters even with custom separator
    assert is_slug("My_blog_post", separator="_") is False
    # Invalid because of leading custom separator
    assert is_slug("_my_blog_post", separator="_") is False
    # Invalid because of trailing custom separator
    assert is_slug("my_blog_post_", separator="_") is False
    # Valid slug with numeric characters
    assert is_slug("post-123-456", separator="-") is True

def test_is_slug_non_string_and_empty_input():
    # Non-string input should return False
    assert is_slug(12345) is False
    assert is_slug(None) is False
    # Empty string is not a full string and should return False
    assert is_slug("") is False
