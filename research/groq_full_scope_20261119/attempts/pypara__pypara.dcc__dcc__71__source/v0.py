import pytest
from pypara.dcc import dcc, DCCRegistry, DCC, Currency

# Helper to clear registry between tests
@pytest.fixture(autouse=True)
def clear_registry():
    DCCRegistry._registry.clear()
    yield
    DCCRegistry._registry.clear()

def test_dcc_registration_and_attributes():
    # Define a simple day count fraction calculator
    def simple_dcfc(start, end):
        return 1.0

    # Register with name, alternative names, and currencies
    alt_names = {"ACT/360", "Actual/360"}
    ccys = {Currency("USD"), Currency("EUR")}

    decorated = dcc("ACT/360", altnames=alt_names, ccys=ccys)(simple_dcfc)

    # The decorated function should have the __dcc attribute
    assert hasattr(decorated, "__dcc")
    dcc_instance = getattr(decorated, "__dcc")
    assert isinstance(dcc_instance, DCC)

    # The DCC instance should have the correct properties
    assert dcc_instance.name == "ACT/360"
    assert dcc_instance.altnames == alt_names
    assert dcc_instance.ccys == ccys
    assert dcc_instance.func is simple_dcfc

    # The registry should contain the new DCC
    assert dcc_instance in DCCRegistry._registry
    # The registry should map the name to the DCC
    assert DCCRegistry._registry["ACT/360"] is dcc_instance
    # Alternative names should also map to the same DCC
    for alt in alt_names:
        assert DCCRegistry._registry[alt] is dcc_instance

def test_dcc_registration_without_optional_arguments():
    # Define a simple day count fraction calculator
    def simple_dcfc(start, end):
        return 2.0

    # Register with only the mandatory name
    decorated = dcc("30/360")(simple_dcfc)

    # The decorated function should have the __dcc attribute
    assert hasattr(decorated, "__dcc")
    dcc_instance = getattr(decorated, "__dcc")
    assert isinstance(dcc_instance, DCC)

    # The DCC instance should have empty sets for altnames and ccys
    assert dcc_instance.altnames == set()
    assert dcc_instance.ccys == set()

    # The registry should contain the new DCC
    assert dcc_instance in DCCRegistry._registry
    assert DCCRegistry._registry["30/360"] is dcc_instance

def test_dcc_registration_duplicate_name_raises():
    # Define two simple calculators
    def dcfc_a(start, end):
        return 3.0

    def dcfc_b(start, end):
        return 4.0

    # Register first calculator
    dcc("ACT/365")(dcfc_a)

    # Attempt to register second calculator with the same name should raise ValueError
    with pytest.raises(ValueError):
        dcc("ACT/365")(dcfc_b)
