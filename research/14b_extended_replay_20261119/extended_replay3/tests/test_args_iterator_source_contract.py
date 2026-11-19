
import pytest
from genty.genty_args import GentyArgs

def test_gentyargs_args_property():
    # Test with no arguments
    genty_args = GentyArgs()
    assert genty_args.args == ()

    # Test with positional arguments
    genty_args = GentyArgs(1, 2, 3)
    assert genty_args.args == (1, 2, 3)

    # Test with keyword arguments
    genty_args = GentyArgs(a=1, b=2)
    assert genty_args.args == ()

    # Test with both positional and keyword arguments
    genty_args = GentyArgs(1, 2, a=1, b=2)
    assert genty_args.args == (1, 2)

def test_gentyargs_iter_method():
    # Test with no arguments
    genty_args = GentyArgs()
    assert list(genty_args) == []

    # Test with positional arguments
    genty_args = GentyArgs(1, 2, 3)
    assert list(genty_args) == ['1', '2', '3']

    # Test with keyword arguments
    genty_args = GentyArgs(a=1, b=2)
    assert list(genty_args) == ['a=1', 'b=2']

    # Test with both positional and keyword arguments
    genty_args = GentyArgs(1, 2, a=1, b=2)
    assert list(genty_args) == ['1', '2', 'a=1', 'b=2']
