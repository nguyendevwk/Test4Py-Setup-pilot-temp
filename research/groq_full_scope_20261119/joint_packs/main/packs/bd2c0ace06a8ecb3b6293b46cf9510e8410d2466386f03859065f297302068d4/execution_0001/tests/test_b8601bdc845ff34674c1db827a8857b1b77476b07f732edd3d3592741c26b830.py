import pytest
from flutes.structure import reverse_map

def test_reverse_map_basic():
    # Normal case: mapping of words to indices
    words = ["apple", "banana", "cherry"]
    word_to_id = {word: idx for idx, word in enumerate(words)}
    id_to_word = reverse_map(word_to_id)
    assert id_to_word == words
    # Ensure the returned list contains the same elements
    assert set(id_to_word) == set(words)
    # Check that the indices correspond correctly
    for idx, word in enumerate(id_to_word):
        assert word_to_id[word] == idx

def test_reverse_map_empty():
    # Boundary case: empty dictionary
    empty_dict = {}
    result = reverse_map(empty_dict)
    assert result == []
    assert isinstance(result, list)

def test_reverse_map_unsorted_keys():
    # Test that the function correctly orders items by their id values
    mapping = {"c": 2, "a": 0, "b": 1}
    result = reverse_map(mapping)
    assert result == ["a", "b", "c"]
    # Verify that the mapping is preserved
    for idx, key in enumerate(result):
        assert mapping[key] == idx
