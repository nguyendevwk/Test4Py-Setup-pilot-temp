import pytest
from py_backwards.transformers.six_moves import SixMovesTransformer

def test_rewrites_contains_expected_mapping():
    # The rewrites attribute should be an iterable of tuples (original, replacement)
    rewrites = list(SixMovesTransformer.rewrites)
    # Verify that a known moved attribute is present in the rewrites
    # For example, 'StringIO' from 'cStringIO' should be rewritten to 'six.moves.StringIO'
    expected = ('StringIO', 'six.moves.StringIO')
    assert expected in rewrites, f"Expected rewrite {expected} not found in rewrites"

def test_dependencies_include_six():
    # The transformer should declare a dependency on the 'six' package
    assert 'six' in SixMovesTransformer.dependencies, "Dependency 'six' not declared"

def test_rewrites_is_non_empty_and_unique():
    # Ensure that rewrites is non-empty and contains unique entries
    rewrites = list(SixMovesTransformer.rewrites)
    assert rewrites, "Rewrites should not be empty"
    # Check that each original module name appears only once
    originals = [orig for orig, _ in rewrites]
    assert len(originals) == len(set(originals)), "Duplicate original module names found in rewrites"
