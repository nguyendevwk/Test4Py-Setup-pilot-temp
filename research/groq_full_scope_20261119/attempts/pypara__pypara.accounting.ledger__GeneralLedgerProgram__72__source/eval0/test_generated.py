import inspect
import pytest
from datetime import date

from pypara.accounting.ledger import GeneralLedgerProgram
from pypara.accounting.zeitgeist import DateRange


def test_general_ledger_program_is_protocol():
    """The imported GeneralLedgerProgram should be a typing.Protocol subclass."""
    assert isinstance(GeneralLedgerProgram, type)
    assert issubclass(GeneralLedgerProgram, type)
    # Protocols are not instantiable
    with pytest.raises(TypeError):
        GeneralLedgerProgram()


def test_dummy_program_conforms_and_returns_value(tmp_path):
    """A dummy class that implements the Protocol should be callable and return the expected value."""
    # Create a simple DateRange for the test
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))

    class DummyProgram(GeneralLedgerProgram[int]):
        def __call__(self, period: DateRange) -> int:
            return 42

    dummy = DummyProgram()
    result = dummy(period)
    assert result == 42, "DummyProgram should return the hardcoded value 42"


def test_general_ledger_program_signature():
    """The __call__ method of the Protocol should accept a DateRange argument."""
    sig = inspect.signature(GeneralLedgerProgram.__call__)
    params = list(sig.parameters.values())
    # The first parameter is 'self', the second should be 'period'
    assert len(params) == 2
    period_param = params[1]
    assert period_param.name == "period"
    assert period_param.annotation is DateRange
    # The return annotation should be a generic type placeholder
    assert period_param.annotation is DateRange
