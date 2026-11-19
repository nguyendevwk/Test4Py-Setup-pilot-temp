import datetime
from decimal import Decimal
from typing import Iterable, List, Protocol, TypeVar

import pytest

from pypara.accounting.ledger import (
    compile_general_ledger_program,
    GeneralLedger,
    GeneralLedgerProgram,
)
from pypara.accounting.journaling import ReadJournalEntries, JournalEntry, Posting
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.commons.zeitgeist import DateRange
from pypara.accounting.commons.numbers import Amount, Quantity

# Define a concrete type for the generic parameter used in the tests
_T = TypeVar("_T", bound=Account)


class DummyReadInitialBalances(Protocol):
    def __call__(self, period: DateRange) -> List[Balance[_T]]: ...


def _make_account(name: str) -> Account:
    """Create a simple Account instance with a unique name."""
    return Account(name=name, description="Test account", type="Asset")


def _make_balance(account: Account, amount: Decimal) -> Balance[Account]:
    return Balance(account=account, amount=Amount(amount))


def _make_posting(account: Account, amount: Decimal) -> Posting[Account]:
    return Posting(account=account, amount=Amount(amount))


def _make_journal_entry(date: datetime.date, postings: List[Posting[Account]]) -> JournalEntry[Account]:
    return JournalEntry(date=date, postings=postings)


@pytest.fixture
def sample_period() -> DateRange:
    return DateRange(start=datetime.date(2023, 1, 1), end=datetime.date(2023, 12, 31))


def test_compile_general_ledger_program_returns_ledger_with_balances_and_entries(
    sample_period: DateRange,
):
    """Verify that the compiled program returns a GeneralLedger containing the expected balances and journal entries."""
    # Arrange: create a simple initial balance and a single journal entry
    account = _make_account("Cash")
    initial_balance = _make_balance(account, Decimal("1000.00"))

    def read_initial_balances(_: DateRange) -> List[Balance[Account]]:
        return [initial_balance]

    entry = _make_journal_entry(
        date=datetime.date(2023, 6, 15),
        postings=[
            _make_posting(account, Decimal("-200.00")),
            _make_posting(account, Decimal("200.00")),
        ],
    )

    def read_journal_entries(_: DateRange) -> Iterable[JournalEntry[Account]]:
        return [entry]

    # Act: compile and run the program
    program: GeneralLedgerProgram[Account] = compile_general_ledger_program(
        read_initial_balances, read_journal_entries
    )
    ledger: GeneralLedger[Account] = program(sample_period)

    # Assert: the ledger contains the initial balance and the journal entry
    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == sample_period
    assert ledger.initial_balances == [initial_balance]
    assert ledger.journal_entries == [entry]
    # The ledger should also compute the closing balances correctly
    closing_balance = ledger.closing_balances[account]
    assert closing_balance.amount == Decimal("1000.00")  # unchanged because debits and credits cancel


def test_compile_general_ledger_program_handles_empty_initial_balances_and_entries(
    sample_period: DateRange,
):
    """Verify that the program works correctly when there are no initial balances or journal entries."""
    # Arrange: no initial balances and no journal entries
    def read_initial_balances(_: DateRange) -> List[Balance[Account]]:
        return []

    def read_journal_entries(_: DateRange) -> Iterable[JournalEntry[Account]]:
        return []

    # Act: compile and run the program
    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)
    ledger = program(sample_period)

    # Assert: the ledger should be empty but still valid
    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == sample_period
    assert ledger.initial_balances == []
    assert ledger.journal_entries == []
    assert ledger.closing_balances == {}


def test_compile_general_ledger_program_raises_on_inconsistent_postings(
    sample_period: DateRange,
):
    """Verify that the program raises an exception when a journal entry has unbalanced postings."""
    account = _make_account("Revenue")
    # Create an entry with mismatched debits and credits
    entry = _make_journal_entry(
        date=datetime.date(2023, 3, 10),
        postings=[
            _make_posting(account, Decimal("500.00")),
            _make_posting(account, Decimal("-300.00")),
        ],
    )

    def read_initial_balances(_: DateRange) -> List[Balance[Account]]:
        return []

    def read_journal_entries(_: DateRange) -> Iterable[JournalEntry[Account]]:
        return [entry]

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)

    # The build_general_ledger function (called inside the program) should raise a ValueError
    # when the postings are not balanced.
    with pytest.raises(ValueError):
        program(sample_period)
