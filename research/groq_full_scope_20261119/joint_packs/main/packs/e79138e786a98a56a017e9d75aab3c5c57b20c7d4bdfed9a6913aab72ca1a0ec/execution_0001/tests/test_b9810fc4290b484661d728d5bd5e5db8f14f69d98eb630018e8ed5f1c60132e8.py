import pytest
from mimesis.providers.choice import Choice


def test_choice_single_element_and_sequence_type():
    """Test that a single element is returned and the type matches the input."""
    provider = Choice()
    # Single element from a list
    result_list = provider(items=[1, 2, 3])
    assert result_list in [1, 2, 3]
    # Single element from a tuple
    result_tuple = provider(items=("x", "y", "z"))
    assert result_tuple in ("x", "y", "z")
    # Single element from a string
    result_str = provider(items="abc")
    assert result_str in "abc"


def test_choice_with_length_and_unique_constraint():
    """Test that a sequence of the requested length is returned and unique constraint works."""
    provider = Choice()
    # Length 3 from a list, not unique
    seq = provider(items=[1, 2, 3], length=3)
    assert isinstance(seq, list)
    assert len(seq) == 3
    # Unique constraint: enough unique elements
    unique_seq = provider(items=[1, 2, 3], length=3, unique=True)
    assert isinstance(unique_seq, list)
    assert len(unique_seq) == 3
    assert len(set(unique_seq)) == 3
    # Unique constraint: not enough unique elements should raise ValueError
    with pytest.raises(ValueError, match="not enough unique elements"):
        provider(items=[1, 1, 2], length=3, unique=True)


def test_choice_string_length_and_type_preservation():
    """Test that string input returns a string of the correct length."""
    provider = Choice()
    # Length 4 from a string
    result = provider(items="abcd", length=4)
    assert isinstance(result, str)
    assert len(result) == 4
    # Ensure all characters are from the original string
    for ch in result:
        assert ch in "abcd"
