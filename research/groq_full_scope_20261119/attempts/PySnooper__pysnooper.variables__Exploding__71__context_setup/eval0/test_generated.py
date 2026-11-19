import pytest
from pysnooper.variables import Exploding, utils

# Helper object with attributes and slots
class SlotObj:
    __slots__ = ('a', 'b')
    def __init__(self):
        self.a = 1
        self.b = 2

def test_exploding_with_mapping():
    # Mapping: dict
    source = "d"
    d = {'x': 10, 'y': 20}
    var = Exploding(source)
    # Simulate frame locals
    frame = type('Frame', (), {'f_globals': {}, 'f_locals': {'d': d}})
    items = var.items(frame)
    # Expect source and each key/value pair
    expected = [
        ('d', utils.get_shortish_repr(d)),
        ('d[x]', utils.get_shortish_repr(10)),
        ('d[y]', utils.get_shortish_repr(20)),
    ]
    assert items == expected

def test_exploding_with_sequence_and_slice():
    # Sequence: list
    source = "lst"
    lst = [100, 200, 300]
    var = Exploding(source)
    frame = type('Frame', (), {'f_globals': {}, 'f_locals': {'lst': lst}})
    # Slice to get first two elements
    sliced_var = var[0:2]
    items = sliced_var.items(frame)
    expected = [
        ('lst', utils.get_shortish_repr(lst)),
        ('lst[0]', utils.get_shortish_repr(100)),
        ('lst[1]', utils.get_shortish_repr(200)),
    ]
    assert items == expected

def test_exploding_with_object_attributes_and_exclusion():
    # Object with __dict__ and __slots__
    source = "obj"
    obj = SlotObj()
    var = Exploding(source, exclude=('b',))
    frame = type('Frame', (), {'f_globals': {}, 'f_locals': {'obj': obj}})
    items = var.items(frame)
    # Should include 'a' but exclude 'b'
    expected = [
        ('obj', utils.get_shortish_repr(obj)),
        ('obj.a', utils.get_shortish_repr(1)),
    ]
    assert items == expected
