import random
import pytest
from string_utils.manipulation import shuffle
from string_utils.errors import InvalidInputError

def test_shuffle_randomness_and_consistency(tmp_path):
    # Seed the RNG to make the test deterministic
    random.seed(42)
    original = "abcdefg"
    shuffled = shuffle(original)
    # The shuffled string should have the same length
    assert len(shuffled) == len(original)
    # The shuffled string should contain the same characters (multiset equality)
    assert sorted(shuffled) == sorted(original)
    # With the seed set, the result should be reproducible
    assert shuffled == "gfeabcd"

def test_shuffle_empty_string():
    # Shuffling an empty string should return an empty string
    assert shuffle("") == ""

def test_shuffle_invalid_input():
    # Passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        shuffle(12345)
