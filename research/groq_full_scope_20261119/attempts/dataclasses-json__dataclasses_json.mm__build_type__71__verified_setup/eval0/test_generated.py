import warnings
import pytest
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, List, Tuple

from marshmallow import fields
from dataclasses_json import dataclass_json
from dataclasses_json.mm import build_type
from dataclasses_json.core import _is_supported_generic
from dataclasses_json.utils import _is_collection

# Helper mixin used by build_type
class Mixin:
    pass

# 1. Test nested dataclass handling
@dataclass_json
@dataclass
class Inner(Mixin):
    x: int

@dataclass_json
@dataclass
class Outer:
    inner: Inner

def test_nested_dataclass_field():
    # Build field for Outer.inner
    field_obj = Outer.__dataclass_fields__['inner']
    marsh_field = build_type(field_obj.type, {}, Mixin, field_obj, Outer)
    # Should be a Nested field with correct schema
    assert isinstance(marsh_field, fields.Nested)
    assert marsh_field.schema == Inner.schema()
    # field_many should be False because Inner is not a collection
    assert marsh_field.field_many is False

# 2. Test optional and union field handling
class Color(Enum):
    RED = 1
    GREEN = 2

@dataclass_json
@dataclass
class Sample:
    opt: Optional[int]
    union: Union[int, str]
    enum: Color

def test_optional_union_and_enum_fields():
    # Optional[int]
    opt_field = Sample.__dataclass_fields__['opt']
    opt_marsh = build_type(opt_field.type, {}, Mixin, opt_field, Sample)
    assert isinstance(opt_marsh, fields.Field)
    assert opt_marsh.allow_none is True

    # Union[int, str]
    union_field = Sample.__dataclass_fields__['union']
    union_marsh = build_type(union_field.type, {}, Mixin, union_field, Sample)
    # UnionField is a subclass of Field
    assert isinstance(union_marsh, fields.Field)
    # It should not be a simple Integer or String field
    assert not isinstance(union_marsh, fields.Integer)
    assert not isinstance(union_marsh, fields.String)

    # Enum field
    enum_field = Sample.__dataclass_fields__['enum']
    enum_marsh = build_type(enum_field.type, {}, Mixin, enum_field, Sample)
    assert isinstance(enum_marsh, fields.Enum)
    assert enum_marsh.enum == Color

# 3. Test unknown type warning and fallback to generic Field
@dataclass_json
@dataclass
class Unknown:
    data: Tuple[int, ...]

def test_unknown_type_warning_and_fallback(tmp_path):
    # Build field for Unknown.data which is a Tuple[int, ...]
    data_field = Unknown.__dataclass_fields__['data']
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        marsh_field = build_type(data_field.type, {}, Mixin, data_field, Unknown)
        # No warning should be issued for known tuple type
        assert len(w) == 0
    # The returned field should be a Tuple field
    assert isinstance(marsh_field, fields.Tuple)
    # Ensure it accepts variable length tuples of integers
    assert marsh_field._args[0].__class__ == fields.Integer
    # Now test an truly unknown type
    @dataclass_json
    @dataclass
    class Bad:
        foo: set  # set is not a supported type

    bad_field = Bad.__dataclass_fields__['foo']
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        bad_marsh = build_type(bad_field.type, {}, Mixin, bad_field, Bad)
        # Warning should be emitted for unknown type
        assert any("Unknown type" in str(warn.message) for warn in w)
    assert isinstance(bad_marsh, fields.Field)
