import pytest
from mimesis.providers.choice import Choice


def test_choice_single_and_sequence_return_types():
    """Test that a single element is returned when length=0 and a sequence
    of the same type is returned when length>0."""
    provider = Choice()
    # Single element from list
    result = provider(items=[1, 2, 3])
    assert result in [1, 2, 3]
    # Sequence of length 2 from list
    seq = provider(items=[1, 2, 3], length=2)
    assert isinstance(seq, list)
    assert len(seq) == 2
    assert all(item in [1, 2, 3] for item in seq)
    # Sequence of length 3 from tuple
    tup = provider(items=("a", "b", "c"), length=3)
    assert isinstance(tup, tuple)
    assert len(tup) == 3
    assert all(item in ("a", "b", "c") for item in tup)
    # Sequence of length 4 from string
    s = provider(items="abc", length=4)
    assert isinstance(s, str)
    assert len(s) == 4
    assert all(ch in "abc" for ch in s)


def test_choice_unique_and_insufficient_elements():
    """Test that unique=True works and raises ValueError when not enough
    unique elements are available."""
    provider = Choice()
    # Unique selection with enough unique items
    unique_seq = provider(items=[1, 2, 3, 4], length=3, unique=True)
    assert isinstance(unique_seq, list)
    assert len(unique_seq) == 3
    assert len(set(unique_seq)) == 3
    # Unique selection with insufficient unique items
    with pytest.raises(ValueError, match="not enough unique elements"):
        provider(items=[1, 1, 2], length=3, unique=True)


def test_choice_invalid_arguments():
    """Test that invalid arguments raise the appropriate exceptions."""
    provider = Choice()
    # Non-sequence items
    with pytest.raises(TypeError, match="must be a sequence"):
        provider(items=123, length=1)
    # Empty sequence
    with pytest.raises(ValueError, match="non-empty sequence"):
        provider(items=[], length=1)
    # Negative length
    with pytest.raises(ValueError, match="non-negative integer"):
        provider(items=[1, 2, 3], length=-1)
