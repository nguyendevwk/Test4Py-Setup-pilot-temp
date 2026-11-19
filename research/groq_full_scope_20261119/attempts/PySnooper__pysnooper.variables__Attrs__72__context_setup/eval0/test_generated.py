import inspect
import pytest
from pysnooper.variables import Attrs
from pysnooper import utils

# Helper class with both __dict__ and __slots__
class SlotDict:
    __slots__ = ('slot_attr',)
    def __init__(self):
        self.slot_attr = 'slot_value'
        self.dict_attr = 'dict_value'

# Helper class with a property that raises an exception
class BadAttr:
    @property
    def bad(self):
        raise RuntimeError("bad property")

def test_attrs_normal_behavior(tmp_path):
    """Attrs should capture both dict and slot attributes."""
    obj = SlotDict()
    var = Attrs("obj")
    # Capture the current frame where obj is defined
    frame = inspect.currentframe()
    try:
        items = var.items(frame, normalize=False)
    finally:
        frame = None
    # First item is the source itself
    assert items[0][0] == "obj"
    assert items[0][1] == utils.get_shortish_repr(obj, normalize=False)
    # Remaining items should include both dict and slot attributes
    keys = {key for key, _ in items[1:]}
    assert '.slot_attr' in keys
    assert '.dict_attr' in keys
    # Verify the values are correctly represented
    values = {key: val for key, val in items[1:]}
    assert values['.slot_attr'] == utils.get_shortish_repr('slot_value', normalize=False)
    assert values['.dict_attr'] == utils.get_shortish_repr('dict_value', normalize=False)

def test_attrs_exclusion(tmp_path):
    """Attrs should skip excluded keys."""
    obj = SlotDict()
    var = Attrs("obj", exclude=('slot_attr',))
    frame = inspect.currentframe()
    try:
        items = var.items(frame, normalize=False)
    finally:
        frame = None
    keys = {key for key, _ in items[1:]}
    assert '.slot_attr' not in keys
    assert '.dict_attr' in keys

def test_attrs_error_handling(tmp_path):
    """Attrs should ignore attributes that raise exceptions."""
    obj = BadAttr()
    var = Attrs("obj")
    frame = inspect.currentframe()
    try:
        items = var.items(frame, normalize=False)
    finally:
        frame = None
    # Only the source itself should be present; no attribute items
    assert len(items) == 1
    assert items[0][0] == "obj"
