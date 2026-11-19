import pytest
from typesystem import Schema, String, ValidationError
from typesystem.schemas import Reference
from typesystem.base import Definitions


class Person(Schema):
    name = String()


class Company(Schema):
    name = String()
    employee = Reference(to="Person", definitions=Definitions({"Person": Person}))


def test_reference_validates_nested_schema():
    data = {"name": "Acme Corp", "employee": {"name": "Alice"}}
    company = Company.validate(data)
    assert isinstance(company, Company)
    assert company.name == "Acme Corp"
    assert isinstance(company.employee, Person)
    assert company.employee.name == "Alice"


def test_reference_allows_null_when_allowed():
    class NullableCompany(Schema):
        name = String()
        employee = Reference(
            to="Person",
            definitions=Definitions({"Person": Person}),
            allow_null=True,
        )

    data = {"name": "Acme Corp", "employee": None}
    company = NullableCompany.validate(data)
    assert company.employee is None


def test_reference_raises_error_on_null_when_not_allowed():
    data = {"name": "Acme Corp", "employee": None}
    with pytest.raises(ValidationError) as excinfo:
        Company.validate(data)
    assert "May not be null." in str(excinfo.value)
