import pytest
from py_backwards.transformers.yield_from import yield_from

def test_yield_from_normal_sequence(tmp_path):
    # Create a simple generator that yields numbers 1, 2, 3
    def simple_gen():
        for i in range(1, 4):
            yield i
    assignment = []
    # Collect yielded values
    yielded = list(yield_from(simple_gen(), None, assignment))
    # Assert that all values were yielded
    assert yielded == [1, 2, 3]
    # After exhaustion, assignment should be extended (empty list in this case)
    assert assignment == []

def test_yield_from_empty_generator(tmp_path):
    # Generator that yields nothing
    def empty_gen():
        if False:
            yield
    assignment = []
    yielded = list(yield_from(empty_gen(), None, assignment))
    # No values should be yielded
    assert yielded == []
    # Assignment should still be extended (no change)
    assert assignment == []

def test_yield_from_non_iterable_raises(tmp_path):
    # Passing a non-iterable should raise TypeError from iter()
    assignment = []
    with pytest.raises(TypeError):
        list(yield_from(42, None, assignment))
