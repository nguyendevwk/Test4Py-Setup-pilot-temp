import pytest
from collections import Counter
from string_utils.manipulation import shuffle
from string_utils.errors import InvalidInputError


def test_shuffle_preserves_characters_and_length():
    """Normal case: shuffled string has same characters and length."""
    original = "hello world"
    shuffled = shuffle(original)
    assert isinstance(shuffled, str)
    assert len(shuffled) == len(original)
    assert Counter(shuffled) == Counter(original)


def test_shuffle_empty_string_returns_empty():
    """Boundary case: shuffling an empty string returns an empty string."""
    assert shuffle("") == ""


def test_shuffle_invalid_input_raises_error():
    """Error case: passing a non-string raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        shuffle(12345)
