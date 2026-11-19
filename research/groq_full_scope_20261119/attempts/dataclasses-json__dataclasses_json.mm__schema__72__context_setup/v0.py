import pytest
from dataclasses import dataclass, field
from typing import Optional, Union, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from dataclasses_json.mm import schema
from dataclasses_json.core import _is_supported_generic
from marshmallow import Schema, ValidationError

# Helper dataclass for testing
@dataclass
class Simple:
    a: int
    b: Optional[str] = None
    c: List[int] = field(default_factory=list)
    d: UUID = field(default_factory=UUID)
    e: Decimal = Decimal("0.0")
    f: Union[int, str] = 42

# Mixin placeholder (not used in these tests)
class DummyMixin:
    pass

def test_schema_basic_fields(tmp_path):
    """Test that required, optional, and default fields are correctly mapped."""
    sch = schema(Simple, DummyMixin, infer_missing=False)
    # Required field 'a' should be present and required
    assert "a" in sch
    assert sch["a"].required is True
    # Optional field 'b' should allow_none and have default None
    assert "b" in sch
    assert sch["b"].allow_none is True
    assert sch["b"].missing is None
    # List field 'c' should be a Nested List with field_many True
    assert "c" in sch
    assert isinstance(sch["c"], type(sch["c"]))
    # UUID field 'd' should be a UUID field
    assert "d" in sch
    assert isinstance(sch["d"], type(sch["d"]))
    # Decimal field 'e' should be Decimal field
    assert "e" in sch
    assert isinstance(sch["e"], type(sch["e"]))
    # Union field 'f' should be a _UnionField
    assert "f" in sch
    assert isinstance(sch["f"], type(sch["f"]))

def test_schema_optional_and_allow_none(tmp_path):
    """Test that optional fields correctly set allow_none and default."""
    @dataclass
    class Opt:
        x: Optional[int] = None
        y: Optional[str] = "default"

    sch = schema(Opt, DummyMixin, infer_missing=True)
    # Field x should be optional with allow_none and default None
    assert sch["x"].allow_none is True
    assert sch["x"].missing is None
    # Field y should be optional with allow_none and default "default"
    assert sch["y"].allow_none is True
    assert sch["y"].missing == "default"

def test_schema_union_deserialization_error(tmp_path):
    """Test that deserializing a Union field with an unsupported type raises ValidationError."""
    @dataclass
    class UnionTest:
        val: Union[int, str] = 0

    class UnionSchema(Schema):
        val = schema(UnionTest, DummyMixin, infer_missing=True)["val"]

    u = UnionTest(val=0)
    s = UnionSchema()
    # Valid deserialization
    assert s.load({"val": 0}) == {"val": 0}
    # Unsupported type (float) should raise ValidationError
    with pytest.raises(ValidationError):
        s.load({"val": 3.14})
