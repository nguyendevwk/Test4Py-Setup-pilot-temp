import pytest
from flutes.structure import reverse_map

def test_reverse_map_basic():
    """Normal case: mapping of words to ids."""
    words = ['apple', 'banana', 'cherry']
    word_to_id = {word: idx for idx, word in enumerate(words)}
    id_to_word = reverse_map(word_to_id)
    assert id_to_word == words
    # Ensure that the list length matches the number of items
    assert len(id_to_word) == len(words)

def test_reverse_map_empty():
    """Boundary case: empty dictionary should return an empty list."""
    empty_dict = {}
    result = reverse_map(empty_dict)
    assert result == []
    assert isinstance(result, list)

def test_reverse_map_non_dict_input():
    """Error case: passing a non-dict should raise an AttributeError."""
    with pytest.raises(AttributeError):
        reverse_map(['a', 'b', 'c'])  # list has no .items() method
