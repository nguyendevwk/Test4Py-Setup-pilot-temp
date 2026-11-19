import pytest
from mimesis.providers.choice import Choice


def test_choice_returns_single_element_when_length_zero():
    """When length is 0, a single random element is returned."""
    provider = Choice()
    items = ["apple", "banana", "cherry"]
    result = provider(items=items, length=0)
    assert result in items
    # The result should be a single element, not a list or tuple
    assert not isinstance(result, (list, tuple, str))


def test_choice_unique_raises_value_error_for_insufficient_unique_elements():
    """Unique=True with length greater than number of unique items raises ValueError."""
    provider = Choice()
    items = ["a", "a", "b"]  # only two unique items
    with pytest.raises(ValueError) as excinfo:
        provider(items=items, length=3, unique=True)
    assert "not enough unique elements" in str(excinfo.value)


def test_choice_raises_type_error_for_non_sequence_items():
    """Providing a non-sequence (e.g., int) raises TypeError."""
    provider = Choice()
    with pytest.raises(TypeError) as excinfo:
        provider(items=42, length=1)
    assert "**items** must be a sequence" in str(excinfo.value)
