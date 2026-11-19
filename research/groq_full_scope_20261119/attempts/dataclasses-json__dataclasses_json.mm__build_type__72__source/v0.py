import warnings
import pytest
from dataclasses import dataclass, field as dc_field
from enum import Enum
from typing import Optional, Tuple, Union

from dataclasses_json.mm import build_type
from dataclasses_json import dataclass_json
from marshmallow import fields

# Helper mixin used by build_type
class Mixin:
    pass

# 1. Test nested dataclass handling
@dataclass_json
@dataclass
class Inner(Mixin):
    x: int

@dataclass
class Outer:
    inner: Inner

def test_nested_dataclass_field():
    # Build field for Outer.inner
    field_obj = build_type(Outer.__annotations__['inner'], {}, Mixin, Outer.__dataclass_fields__['inner'], Outer)
    # Should be a Nested field pointing to Inner.schema()
    assert isinstance(field_obj, fields.Nested)
    assert field_obj.schema_class == Inner.schema()
    # field_many should be False because Inner is not a collection
    assert field_obj.metadata.get('field_many', False) is False

# 2. Test optional and tuple handling
@dataclass
class TupleHolder:
    opt: Optional[int]
    tup: Tuple[int, ...]
    enum: Enum  # placeholder, will be overridden

class Color(Enum):
    RED = 1
    GREEN = 2

def test_optional_and_tuple_and_enum():
    # Override enum field type
    TupleHolder.__annotations__['enum'] = Color
    # Build optional field
    opt_field = build_type(TupleHolder.__annotations__['opt'], {}, Mixin, TupleHolder.__dataclass_fields__['opt'], TupleHolder)
    assert isinstance(opt_field, fields.Field)
    assert opt_field.metadata.get('allow_none', False) is True

    # Build tuple field
    tup_field = build_type(TupleHolder.__annotations__['tup'], {}, Mixin, TupleHolder.__dataclass_fields__['tup'], TupleHolder)
    assert isinstance(tup_field, fields.Tuple)
    # Tuple should have a single element type int
    assert len(tup_field.fields) == 1
    assert isinstance(tup_field.fields[0], fields.Integer)

    # Build enum field
    enum_field = build_type(TupleHolder.__annotations__['enum'], {}, Mixin, TupleHolder.__dataclass_fields__['enum'], TupleHolder)
    assert isinstance(enum_field, fields.Enum)
    assert enum_field.enum == Color
    assert enum_field.by_value is True

# 3. Test union handling and warning for unknown type
@dataclass
class UnionHolder:
    union: Union[int, str, None]

def test_union_and_unknown_type_warning():
    # Build union field
    union_field = build_type(UnionHolder.__annotations__['union'], {}, Mixin, UnionHolder.__dataclass_fields__['union'], UnionHolder)
    # Should be a custom _UnionField type from dataclasses_json
    from dataclasses_json.core import _UnionField
    assert isinstance(union_field, _UnionField)
    # The union descriptor should map int and str to corresponding fields
    assert set(union_field.union_desc.keys()) == {int, str}

    # Test warning for unknown type
    class Unknown:
        pass
    with pytest.warns(UserWarning) as record:
        unknown_field = build_type(Unknown, {}, Mixin, None, None)
    assert any("Unknown type" in str(w.message) for w in record)
    assert isinstance(unknown_field, fields.Field)
