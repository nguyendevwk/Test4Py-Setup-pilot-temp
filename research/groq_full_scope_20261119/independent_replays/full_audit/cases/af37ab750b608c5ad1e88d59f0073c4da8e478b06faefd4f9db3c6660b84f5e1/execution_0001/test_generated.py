import pytest
from flutes.structure import reverse_map

def test_reverse_map_basic():
    """Normal case: mapping from items to unique consecutive ids."""
    words = ["apple", "banana", "cherry"]
    word_to_id = {word: idx for idx, word in enumerate(words)}
    id_to_word = reverse_map(word_to_id)
    assert id_to_word == words
    # Ensure the returned list has the same length as the input dict
    assert len(id_to_word) == len(word_to_id)

def test_reverse_map_empty():
    """Boundary case: empty dictionary should return an empty list."""
    empty_dict = {}
    result = reverse_map(empty_dict)
    assert result == []
    assert isinstance(result, list)

def test_reverse_map_non_permutation():
    """Error-like case: duplicate ids lead to duplicate items in the output list."""
    # Two different items share the same id
    d = {"x": 0, "y": 0, "z": 1}
    result = reverse_map(d)
    # The sorted order will place both items with id 0 before id 1
    assert result == ["x", "y", "z"] or result == ["y", "x", "z"]
    # The length of the result should match the number of items in the dict
    assert len(result) == len(d)
