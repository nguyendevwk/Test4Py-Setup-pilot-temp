import warnings
import pytest
from dataclasses import dataclass, field
from typing import Optional, Union, List, Tuple
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from dataclasses_json.mm import build_type, _TimestampField, _UnionField, _TupleVarLen
from dataclasses_json import dataclass_json
from marshmallow import Schema, fields

# Helper dataclasses for testing
@dataclass_json
@dataclass
class Inner:
    x: int

@dataclass_json
@dataclass
class Outer:
    inner: Inner
    opt: Optional[int]
    union: Union[int, str]
    lst: List[int]
    tup: Tuple[int, ...]
    uuid: UUID
    dec: Decimal
    ts: datetime

# Test 1: Nested dataclass field is correctly converted to Nested schema
def test_nested_dataclass_field():
    schema = Outer.schema()
    nested_field = schema.fields["inner"]
    assert isinstance(nested_field, fields.Nested)
    assert nested_field.schema.__class__ is Inner.schema().__class__
    # Ensure that nested field is not a plain Field
    assert not isinstance(nested_field, fields.Field)

# Test 2: Optional and Union fields are handled correctly
def test_optional_and_union_fields():
    schema = Outer.schema()
    # Optional field should allow None
    opt_field = schema.fields["opt"]
    assert opt_field.allow_none is True
    # Union field should be an instance of _UnionField
    union_field = schema.fields["union"]
    assert isinstance(union_field, _UnionField)
    # Serialize a value of each union type
    data_int = {"union": 42}
    data_str = {"union": "hello"}
    assert schema.dump(data_int)["union"] == 42
    assert schema.dump(data_str)["union"] == "hello"

# Test 3: Special types (UUID, Decimal, datetime, tuple) are mapped to correct marshmallow fields
def test_special_type_mappings():
    schema = Outer.schema()
    # UUID field
    uuid_field = schema.fields["uuid"]
    assert isinstance(uuid_field, fields.UUID)
    # Decimal field
    dec_field = schema.fields["dec"]
    assert isinstance(dec_field, fields.Decimal)
    # Timestamp field
    ts_field = schema.fields["ts"]
    assert isinstance(ts_field, _TimestampField)
    # Tuple field should be _TupleVarLen for variable length homogeneous tuples
    tup_field = schema.fields["tup"]
    assert isinstance(tup_field, _TupleVarLen)
    # List field should be List
    lst_field = schema.fields["lst"]
    assert isinstance(lst_field, fields.List)
