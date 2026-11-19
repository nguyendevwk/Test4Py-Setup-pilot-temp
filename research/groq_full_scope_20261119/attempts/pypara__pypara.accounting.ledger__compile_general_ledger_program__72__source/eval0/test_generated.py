import pytest
from datetime import date

from pypara.accounting.ledger import (
    compile_general_ledger_program,
    build_general_ledger,
    GeneralLedger,
)
from pypara.accounting.zeitgeist import DateRange
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance


def test_compile_program_returns_callable_and_uses_period():
    """The compiled program should be a callable that receives a DateRange and returns a GeneralLedger."""
    # Prepare dummy read functions that record the period they were called with
    called_periods = []

    def read_initial_balances(period: DateRange):
        called_periods.append(("initial", period))
        return {}

    def read_journal_entries(period: DateRange):
        called_periods.append(("journal", period))
        return []

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)

    # Ensure the returned object is callable
    assert callable(program)

    # Create a period and invoke the program
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    ledger = program(period)

    # The ledger should be an instance of GeneralLedger
    assert isinstance(ledger, GeneralLedger)

    # The period should have been passed to both read functions
    assert called_periods == [
        ("initial", period),
        ("journal", period),
    ]


def test_compile_program_propagates_initial_balance_exception():
    """If reading initial balances raises an exception, the program should propagate it."""
    def read_initial_balances(period: DateRange):
        raise RuntimeError("Failed to read initial balances")

    def read_journal_entries(period: DateRange):
        return []

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)

    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    with pytest.raises(RuntimeError, match="Failed to read initial balances"):
        program(period)


def test_compile_program_with_empty_journal_entries():
    """When there are no journal entries, the ledger should contain only the initial balances."""
    # Initial balances for two accounts
    initial_balances = {
        Account("Cash"): Balance(Decimal("1000.00")),
        Account("Revenue"): Balance(Decimal("0.00")),
    }

    def read_initial_balances(period: DateRange):
        return initial_balances

    def read_journal_entries(period: DateRange):
        return []

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)

    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    ledger = program(period)

    # The ledger should contain the same balances as the initial balances
    for account, balance in initial_balances.items():
        assert ledger.get_balance(account) == balance
