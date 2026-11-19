import warnings
import pytest
from dataclasses import dataclass, field as dc_field
from dataclasses import is_dataclass
from typing import Optional, Union, List, Tuple
from uuid import UUID
from enum import Enum
from marshmallow import fields

from dataclasses_json.mm import build_type
from dataclasses_json import dataclass_json

# Helper mixin used by build_type
class Mixin:
    pass

# 1. Test nested dataclass serialization
@dataclass_json
class Inner:
    x: int

@dataclass_json
class Outer:
    inner: Inner
    mixin_field: int

def test_nested_dataclass_field():
    # Build type for a nested dataclass field
    inner_field = Outer.__dataclass_fields__['inner']
    result = build_type(Inner, {}, Mixin, inner_field, Outer)
    assert isinstance(result, fields.Nested)
    # The nested schema should be Inner.schema()
    assert result.schema_class == Inner.schema()
    # field_many should be False because Inner is not a collection
    assert result.metadata.get('field_many') is False

    # Build type for a non-dataclass_json field
    mixin_field = Outer.__dataclass_fields__['mixin_field']
    with pytest.warns(UserWarning) as record:
        result2 = build_type(int, {}, Mixin, mixin_field, Outer)
    assert isinstance(result2, fields.Field)
    assert "Nested dataclass field mixin_field" in str(record[0].message)

# 2. Test optional and union handling
class Color(Enum):
    RED = 1
    GREEN = 2

@dataclass_json
class Sample:
    opt: Optional[int]
    union: Union[int, str]
    enum: Color
    list_of_int: List[int]
    tuple_fixed: Tuple[int, str]
    tuple_varlen: Tuple[int, ...]

def test_optional_union_and_collections():
    # Optional field
    opt_field = Sample.__dataclass_fields__['opt']
    opt_result = build_type(Optional[int], {}, Mixin, opt_field, Sample)
    assert isinstance(opt_result, fields.Field)
    assert opt_result.metadata.get('allow_none') is True

    # Union field
    union_field = Sample.__dataclass_fields__['union']
    union_result = build_type(Union[int, str], {}, Mixin, union_field, Sample)
    assert hasattr(union_result, 'union_desc')
    assert set(union_result.union_desc.keys()) == {int, str}

    # Enum field
    enum_field = Sample.__dataclass_fields__['enum']
    enum_result = build_type(Color, {}, Mixin, enum_field, Sample)
    assert isinstance(enum_result, fields.Enum)
    assert enum_result.enum == Color

    # List field
    list_field = Sample.__dataclass_fields__['list_of_int']
    list_result = build_type(List[int], {}, Mixin, list_field, Sample)
    assert isinstance(list_result, fields.List)
    assert list_result.inner_type == fields.Integer

    # Fixed tuple
    tuple_field = Sample.__dataclass_fields__['tuple_fixed']
    tuple_result = build_type(Tuple[int, str], {}, Mixin, tuple_field, Sample)
    assert isinstance(tuple_result, fields.Tuple)
    assert tuple_result.inner_types == (fields.Integer, fields.String)

    # Variable length tuple
    varlen_field = Sample.__dataclass_fields__['tuple_varlen']
    varlen_result = build_type(Tuple[int, ...], {}, Mixin, varlen_field, Sample)
    assert hasattr(varlen_result, 'inner_type')
    assert varlen_result.inner_type == fields.Integer

# 3. Test unknown type warning and fallback to generic Field
@dataclass_json
class Unknown:
    data: UUID

def test_unknown_type_warning():
    unknown_field = Unknown.__dataclass_fields__['data']
    with pytest.warns(UserWarning) as record:
        result = build_type(UUID, {}, Mixin, unknown_field, Unknown)
    assert isinstance(result, fields.Field)
    assert "Unknown type" in str(record[0].message)
