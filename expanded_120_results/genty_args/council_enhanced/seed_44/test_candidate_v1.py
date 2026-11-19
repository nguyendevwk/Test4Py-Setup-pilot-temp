import pytest
from genty.genty_args import GentyArgs


def test_genty_args_iteration_and_properties():
    """Verify that GentyArgs stores args/kwargs correctly and iterates
    over formatted values in the expected order."""
    g = GentyArgs(1, 2, key='val')

    # Property access should return the original values
    assert isinstance(g.args, tuple)
    assert g.args == (1, 2)
    assert isinstance(g.kwargs, dict)
    assert g.kwargs == {'key': 'val'}

    # Iteration should yield formatted positional args followed by
    # sorted keyword args in "key=value" form
    iterated = list(g)
    assert iterated == ['1', '2', "key='val'"]
