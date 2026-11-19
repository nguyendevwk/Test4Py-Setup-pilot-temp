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
    pair: Tuple[int, str]

def test_optional_and_tuple_fields():
    # Optional[int]
    opt_field = build_type(TupleHolder.__annotations__['opt'], {}, Mixin, TupleHolder.__dataclass_fields__['opt'], TupleHolder)
    assert isinstance(opt_field, fields.Field)
    assert opt_field.metadata.get('allow_none', False) is True

    # Tuple[int, ...] -> variable length tuple
    var_tup_field = build_type(TupleHolder.__annotations__['tup'], {}, Mixin, TupleHolder.__dataclass_fields__['tup'], TupleHolder)
    assert hasattr(var_tup_field, 'inner_type')
    assert var_tup_field.inner_type == int

    # Tuple[int, str] -> fixed length tuple
    pair_field = build_type(TupleHolder.__annotations__['pair'], {}, Mixin, TupleHolder.__dataclass_fields__['pair'], TupleHolder)
    assert isinstance(pair_field, fields.Tuple)
    assert pair_field.inner_types == (int, str)

# 3. Test enum and union handling with warnings
class Color(Enum):
    RED = 1
    GREEN = 2

@dataclass
class UnionHolder:
    color: Color
    data: Union[int, str, None]

def test_enum_and_union_fields():
    # Enum field
    enum_field = build_type(UnionHolder.__annotations__['color'], {}, Mixin, UnionHolder.__dataclass_fields__['color'], UnionHolder)
    assert isinstance(enum_field, fields.Enum)
    assert enum_field.enum == Color
    assert enum_field.by_value is True

    # Union field should warn about unknown type
    with pytest.warns(UserWarning) as record:
        union_field = build_type(UnionHolder.__annotations__['data'], {}, Mixin, UnionHolder.__dataclass_fields__['data'], UnionHolder)
    assert any("Unknown type" in str(w.message) for w in record)
    # The returned field should be a custom UnionField (subclass of fields.Field)
    assert hasattr(union_field, 'union_desc')
    assert set(union_field.union_desc.keys()) == {int, str}
