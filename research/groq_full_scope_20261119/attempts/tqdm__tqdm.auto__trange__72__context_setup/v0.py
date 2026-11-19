import pytest
from tqdm.auto import trange

def test_trange_raises_name_error_on_simple_call():
    """Calling trange without arguments should raise NameError because tqdm is undefined."""
    with pytest.raises(NameError):
        trange(5)

def test_trange_raises_name_error_with_negative_range():
    """Calling trange with a negative start should also raise NameError."""
    with pytest.raises(NameError):
        trange(-5, 0)

def test_trange_raises_name_error_with_kwargs():
    """Calling trange with keyword arguments should raise NameError."""
    with pytest.raises(NameError):
        trange(10, desc="test")
