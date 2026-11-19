import pytest
from mimesis.providers.choice import Choice


def test_choice_single_and_sequence_output():
    """Test that a single element is returned when length=0 and a sequence
    of the same type is returned when length>0."""
    provider = Choice()
    # Single element from list
    result = provider(items=[1, 2, 3])
    assert result in [1, 2, 3]
    # Sequence of length 3 from tuple
    seq = provider(items=("a", "b", "c"), length=3)
    assert isinstance(seq, tuple)
    assert len(seq) == 3
    assert all(ch in ("a", "b", "c") for ch in seq)
    # Sequence of length 4 from string
    seq_str = provider(items="abc", length=4)
    assert isinstance(seq_str, str)
    assert len(seq_str) == 4
    assert all(ch in "abc" for ch in seq_str)


def test_choice_unique_and_insufficient_elements():
    """Test that unique=True works and raises ValueError when not enough unique items."""
    provider = Choice()
    # Unique selection works
    unique_seq = provider(items=[1, 2, 3, 4], length=3, unique=True)
    assert isinstance(unique_seq, list)
    assert len(unique_seq) == 3
    assert len(set(unique_seq)) == 3
    # Insufficient unique elements raise ValueError
    with pytest.raises(ValueError, match="not enough unique elements"):
        provider(items=[1, 1, 2], length=3, unique=True)


def test_choice_invalid_inputs_and_errors():
    """Test that invalid types and negative lengths raise appropriate errors."""
    provider = Choice()
    # Non-sequence items
    with pytest.raises(TypeError, match="must be a sequence"):
        provider(items=42, length=1)
    # Empty sequence
    with pytest.raises(ValueError, match="non-empty sequence"):
        provider(items=[], length=1)
    # Negative length
    with pytest.raises(ValueError, match="non-negative integer"):
        provider(items=[1, 2, 3], length=-1)
