import pytest
from mimesis.providers.choice import Choice


def test_choice_returns_sequence_of_specified_length_and_type(tmp_path):
    """Test that a list of the requested length is returned and contains only
    elements from the original list."""
    provider = Choice()
    items = [1, 2, 3, 4]
    result = provider(items=items, length=3, unique=False)
    assert isinstance(result, list)
    assert len(result) == 3
    assert all(item in items for item in result)


def test_choice_single_element_and_string_handling():
    """Test that a single element is returned when length is 0 and that a
    string input returns a string of the same length."""
    provider = Choice()
    # Single element from a list
    single = provider(items=[10, 20, 30], length=0)
    assert single in [10, 20, 30]
    # String input returns a string of the requested length
    string_result = provider(items="abc", length=2, unique=False)
    assert isinstance(string_result, str)
    assert len(string_result) == 2
    assert all(ch in "abc" for ch in string_result)


def test_choice_unique_error_on_insufficient_elements():
    """Test that a ValueError is raised when unique=True but the number of
    unique items is less than the requested length."""
    provider = Choice()
    items = ["a", "a", "b"]
    with pytest.raises(ValueError) as excinfo:
        provider(items=items, length=3, unique=True)
    assert "not enough unique elements" in str(excinfo.value)
