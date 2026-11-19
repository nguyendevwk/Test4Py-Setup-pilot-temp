import pytest
from string_utils.validation import is_slug

def test_is_slug_valid_and_invalid_cases():
    # Valid slug with default separator
    assert is_slug("my-blog-post-title") is True
    # Invalid because of uppercase letters
    assert is_slug("My-blog-post-title") is False
    # Invalid because of leading separator
    assert is_slug("-my-blog-post") is False
    # Invalid because of trailing separator
    assert is_slug("my-blog-post-") is False
    # Invalid because of consecutive separators
    assert is_slug("my--blog-post") is False
    # Invalid because of non-alphanumeric characters
    assert is_slug("my_blog_post") is False

def test_is_slug_with_custom_separator_and_edge_cases():
    # Valid slug with custom separator
    assert is_slug("my_blog_post", separator="_") is True
    # Invalid because of uppercase letters with custom separator
    assert is_slug("My_blog_post", separator="_") is False
    # Empty string should be invalid
    assert is_slug("") is False
    # Single character slug
    assert is_slug("a") is True
    # Single character with separator should be invalid
    assert is_slug("-", separator="-") is False

def test_is_slug_non_string_inputs():
    # Non-string input should return False
    assert is_slug(12345) is False
    assert is_slug(None) is False
    assert is_slug(["my", "blog"]) is False
    # Even if separator is non-string, function should still handle it gracefully
    assert is_slug("my-blog-post", separator=1) is False
