import random
import pytest
from string_utils.manipulation import shuffle
from string_utils.errors import InvalidInputError

def test_shuffle_preserves_characters_and_length(tmp_path):
    """Shuffle should return a string of the same length with the same characters."""
    original = "hello world"
    # Seed the RNG for deterministic behaviour
    random.seed(42)
    shuffled = shuffle(original)
    assert len(shuffled) == len(original)
    assert sorted(shuffled) == sorted(original)
    # With the seed 42 the expected shuffled string is known
    assert shuffled == "ldro wlehol"

def test_shuffle_empty_string_returns_empty(tmp_path):
    """Shuffling an empty string should return an empty string."""
    assert shuffle("") == ""

def test_shuffle_invalid_input_raises_error():
    """Non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        shuffle(123)
