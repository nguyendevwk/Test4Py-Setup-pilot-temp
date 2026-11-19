import pytest
import typesystem
from typesystem.schemas import Reference, ValidationError

# Define two simple schemas to use with Reference
class Address(typesystem.Schema):
    street = typesystem.String()
    city = typesystem.String()

class Person(typesystem.Schema):
    name = typesystem.String()
    address = Reference(to="Address", definitions=typesystem.schemas.Definitions({"Address": Address}))

def test_reference_validates_nested_schema():
    """Reference should validate a nested schema instance correctly."""
    person_data = {"name": "Alice", "address": {"street": "123 Main St", "city": "Wonderland"}}
    person = Person.validate(person_data)
    assert isinstance(person, Person)
    assert person.name == "Alice"
    assert isinstance(person.address, Address)
    assert person.address.street == "123 Main St"
    assert person.address.city == "Wonderland"

def test_reference_allows_null_when_allowed():
    """Reference should allow None when allow_null is True."""
    class NullablePerson(typesystem.Schema):
        name = typesystem.String()
        address = Reference(to="Address", definitions=typesystem.schemas.Definitions({"Address": Address}), allow_null=True)

    person_data = {"name": "Bob", "address": None}
    person = NullablePerson.validate(person_data)
    assert person.address is None

def test_reference_raises_error_on_null_when_not_allowed():
    """Reference should raise ValidationError when value is None and allow_null is False."""
    class StrictPerson(typesystem.Schema):
        name = typesystem.String()
        address = Reference(to="Address", definitions=typesystem.schemas.Definitions({"Address": Address}))

    person_data = {"name": "Charlie", "address": None}
    with pytest.raises(ValidationError) as excinfo:
        StrictPerson.validate(person_data)
    assert "May not be null." in str(excinfo.value)
