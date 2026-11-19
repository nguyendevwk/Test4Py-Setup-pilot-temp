import pytest
from sty.lib import mute
from sty.primitive import Register


class DummyRegister(Register):
    """A minimal Register subclass that records whether mute was called."""

    def __init__(self):
        super().__init__()
        self.muted = False

    def mute(self):
        self.muted = True


def test_mute_calls_mute_on_all_objects(tmp_path):
    """mute should call the mute method on each Register instance."""
    objs = [DummyRegister() for _ in range(3)]
    mute(*objs)
    assert all(obj.muted for obj in objs), "All objects should be muted"


def test_mute_with_single_object(tmp_path):
    """mute should work with a single Register instance."""
    obj = DummyRegister()
    mute(obj)
    assert obj.muted, "The single object should be muted"


def test_mute_with_non_register_raises_error(tmp_path):
    """mute should raise ValueError when a non-Register object is passed."""
    class NotRegister:
        pass

    not_reg = NotRegister()
    with pytest.raises(ValueError) as excinfo:
        mute(not_reg)
    assert "inherit from the 'Register class'" in str(excinfo.value)


def test_mute_with_mixed_objects_raises_error(tmp_path):
    """mute should raise ValueError if any argument is not a Register."""
    obj1 = DummyRegister()
    obj2 = object()  # not a Register
    with pytest.raises(ValueError):
        mute(obj1, obj2)
    # Ensure that the first object's mute was not called due to early error
    assert not obj1.muted, "First object's mute should not be called if error occurs"


def test_mute_with_no_arguments_does_nothing(tmp_path):
    """mute should accept no arguments and simply return None."""
    result = mute()
    assert result is None, "mute() should return None when called with no arguments"
