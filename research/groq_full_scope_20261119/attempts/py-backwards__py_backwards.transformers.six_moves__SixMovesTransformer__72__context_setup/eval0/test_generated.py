import pytest
from py_backwards.transformers.six_moves import SixMovesTransformer
from py_backwards.transformers.six_moves import _get_rewrites, MovedAttribute, MovedModule

def test_rewrites_contains_expected_mapping():
    """The rewrites list should contain a mapping for a known moved attribute."""
    # Create a known moved attribute: urllib.parse.quote moved to six.moves.urllib.parse.quote
    moved = MovedAttribute(name="quote", old_mod="urllib.parse", new_mod="urllib.parse", old_attr="quote")
    # Generate rewrites for this single move
    rewrites = list(_get_rewrites())
    # Find the tuple that matches the expected mapping
    expected = ("urllib.parse.quote", "six.moves.urllib.parse.quote")
    assert expected in rewrites, f"Expected mapping {expected!r} not found in rewrites"

def test_dependencies_include_six():
    """The transformer should declare a dependency on the 'six' package."""
    assert "six" in SixMovesTransformer.dependencies, "Dependency 'six' missing from SixMovesTransformer"

def test_target_version_tuple():
    """The transformer should target Python 2.7."""
    assert SixMovesTransformer.target == (2, 7), f"Expected target (2, 7), got {SixMovesTransformer.target}"
