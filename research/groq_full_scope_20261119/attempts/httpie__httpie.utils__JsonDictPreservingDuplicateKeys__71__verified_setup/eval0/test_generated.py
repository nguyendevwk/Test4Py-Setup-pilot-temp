import json
import sys
import pytest
from httpie.utils import JsonDictPreservingDuplicateKeys


def test_duplicate_keys_preserved_and_dumped():
    # Create a dict with duplicate keys
    items = [("a", 1), ("b", 2), ("a", 3), ("c", 4)]
    jd = JsonDictPreservingDuplicateKeys(items)

    # The internal items should match the input list
    assert list(jd.items()) == items

    # json.dumps should use the overridden items method and preserve order
    dumped = json.dumps(jd, separators=(",", ":"))
    # Expected JSON string with duplicate keys in the same order
    expected = '{"a":1,"b":2,"a":3,"c":4}'
    assert dumped == expected


def test_supports_sorting_flag_matches_python_version():
    # The flag should be True for Python 3.8+ and False otherwise
    expected = sys.version_info >= (3, 8)
    assert JsonDictPreservingDuplicateKeys.SUPPORTS_SORTING is expected


def test_initialization_with_invalid_items_raises_type_error():
    # Passing a non-iterable (e.g., None) should raise a TypeError when json.dumps is called
    jd = JsonDictPreservingDuplicateKeys(None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        json.dumps(jd)
