import pytest
from mimesis.providers.choice import Choice

# Test 1: Normal single element selection from a list
def test_choice_single_element():
    provider = Choice()
    items = ["apple", "banana", "cherry"]
    # Since the choice is random, we only assert that the result is one of the items
    result = provider(items=items)
    assert result in items
    # Ensure that calling again yields possibly different result
    result2 = provider(items=items)
    assert result2 in items

# Test 2: Length selection with unique constraint from a string
def test_choice_length_unique_string():
    provider = Choice()
    items = "aabbbccccddddd"
    length = 4
    result = provider(items=items, length=length, unique=True)
    # Result should be a string of the requested length
    assert isinstance(result, str)
    assert len(result) == length
    # All characters should be unique
    assert len(set(result)) == length
    # All characters must come from the original items
    assert all(ch in items for ch in result)

# Test 3: Error handling for insufficient unique elements
def test_choice_insufficient_unique_raises():
    provider = Choice()
    items = ["x", "x", "x"]
    length = 2
    with pytest.raises(ValueError) as excinfo:
        provider(items=items, length=length, unique=True)
    assert "not enough unique elements" in str(excinfo.value)
