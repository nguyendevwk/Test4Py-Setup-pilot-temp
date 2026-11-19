import pytest
import types
from pysnooper.variables import Attrs
from pysnooper import utils

# Helper class with both __dict__ and __slots__
class SlotDict:
    __slots__ = ('slot_attr',)
    def __init__(self):
        self.dict_attr = 42
        self.slot_attr = 'slot'

# Helper class with an attribute that raises on access
class BadAttr:
    def __init__(self):
        self.good = 'ok'
    @property
    def bad(self):
        raise RuntimeError('access error')

def test_attrs_collects_dict_and_slots(tmp_path):
    obj = SlotDict()
    var = Attrs('obj')
    # Create a dummy frame with obj in locals
    frame = types.FrameType(
        None, {}, {'obj': obj}, None, None, None, None, None, None, None, None, None, None, None, None
    )
    items = var.items(frame)
    # Expect source and two attributes
    assert items[0] == ('obj', utils.get_shortish_repr(obj))
    # The order of attributes is not guaranteed; check presence
    keys = {key for key, _ in items[1:]}
    assert '.dict_attr' in keys
    assert '.slot_attr' in keys
    # Verify values
    values = {key: val for key, val in items[1:]}
    assert values['.dict_attr'] == utils.get_shortish_repr(42)
    assert values['.slot_attr'] == utils.get_shortish_repr('slot')

def test_attrs_excludes_specified_keys(tmp_path):
    obj = SlotDict()
    var = Attrs('obj', exclude=('slot_attr',))
    frame = types.FrameType(
        None, {}, {'obj': obj}, None, None, None, None, None, None, None, None, None, None, None, None
    )
    items = var.items(frame)
    keys = {key for key, _ in items[1:]}
    assert '.slot_attr' not in keys
    assert '.dict_attr' in keys

def test_attrs_skips_attributes_that_raise(tmp_path):
    obj = BadAttr()
    var = Attrs('obj')
    frame = types.FrameType(
        None, {}, {'obj': obj}, None, None, None, None, None, None, None, None, None, None, None, None
    )
    items = var.items(frame)
    keys = {key for key, _ in items[1:]}
    # 'bad' should be omitted due to exception
    assert '.bad' not in keys
    assert '.good' in keys
    # Ensure no exception propagates
    assert all(isinstance(val, str) for _, val in items)
