import pytest
import typesystem
from typesystem.tokenize.tokenize_yaml import validate_yaml
from typesystem.fields import String, Integer
from typesystem.schemas import Schema


class Person(Schema):
    name = String()
    age = Integer()


def test_validate_yaml_success(tmp_path):
    yaml_content = """
    name: Alice
    age: 30
    """
    value, errors = validate_yaml(yaml_content, Person)
    assert errors == []
    assert isinstance(value, Person)
    assert value.name == "Alice"
    assert value.age == 30


def test_validate_yaml_syntax_error(tmp_path):
    yaml_content = """
    name: Alice
    age: 30
    - invalid
    """
    value, errors = validate_yaml(yaml_content, Person)
    assert value is None
    assert errors
    # The first error should mention a syntax issue near the dash
    assert any("syntax" in e.lower() or "error" in e.lower() for e in errors)


def test_validate_yaml_validation_error(tmp_path):
    yaml_content = """
    name: Bob
    age: not_a_number
    """
    value, errors = validate_yaml(yaml_content, Person)
    assert value is None
    assert errors
    # The error should refer to the age field and type mismatch
    assert any("age" in e.lower() and ("int" in e.lower() or "integer" in e.lower()) for e in errors)
