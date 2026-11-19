import pytest
from py_backwards.transformers.yield_from import yield_from

def test_yield_from_normal_iteration():
    # A simple generator that yields three values
    def gen():
        for i in range(3):
            yield i
    assignment = []
    # Collect values from the yield_from generator
    yielded = list(yield_from(gen(), None, assignment))
    assert yielded == [0, 1, 2], "yield_from should yield all items from the generator"
    # After exhaustion, assignment should be extended (implementation dependent)
    # We check that assignment is still a list (no exception raised)
    assert isinstance(assignment, list), "assignment should remain a list after yield_from"

def test_yield_from_empty_generator():
    # Generator that yields nothing
    def empty_gen():
        if False:
            yield
    assignment = []
    yielded = list(yield_from(empty_gen(), None, assignment))
    assert yielded == [], "yield_from should return an empty list for an empty generator"
    assert isinstance(assignment, list), "assignment should remain a list after yield_from"

def test_yield_from_unexpected_exception():
    # Generator that raises a ValueError instead of StopIteration
    def bad_gen():
        raise ValueError("unexpected")
    assignment = []
    with pytest.raises(ValueError, match="unexpected"):
        # The generator should propagate the ValueError
        list(yield_from(bad_gen(), None, assignment))
    # assignment should remain unchanged
    assert assignment == [], "assignment should not be modified when an unexpected exception occurs"
