import pytest
from datetime import date
from decimal import Decimal
from pypara.accounting.ledger import (
    compile_general_ledger_program,
    GeneralLedgerProgram,
    GeneralLedger,
    ReadInitialBalances,
    ReadJournalEntries,
)
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import JournalEntry, Posting, ReadJournalEntries
from pypara.commons.zeitgeist import DateRange


def _make_account(name: str) -> Account:
    """Convenience factory for an Account with a simple name."""
    return Account(name=name, description="test account")


def _make_balance(amount: Decimal) -> Balance:
    """Convenience factory for a Balance with a single amount."""
    return Balance(amount=amount, currency="USD")


def _make_posting(account: Account, amount: Decimal) -> Posting:
    """Convenience factory for a Posting."""
    return Posting(account=account, amount=amount, currency="USD")


def _make_journal_entry(date_: date, postings: list[Posting]) -> JournalEntry:
    """Convenience factory for a JournalEntry."""
    return JournalEntry(date=date_, postings=postings)


def test_compile_general_ledger_program_normal_behavior(tmp_path):
    """Test that the compiled program correctly aggregates initial balances and journal entries."""
    # Setup accounts and balances
    acc_cash = _make_account("Cash")
    acc_sales = _make_account("Sales")
    initial_balances = {acc_cash: _make_balance(Decimal("1000.00"))}

    # Journal entries: one debit to Cash, one credit to Sales
    entry = _make_journal_entry(
        date=date(2024, 1, 15),
        postings=[
            _make_posting(acc_cash, Decimal("200.00")),
            _make_posting(acc_sales, Decimal("-200.00")),
        ],
    )
    journal_entries = [entry]

    # Define simple readers
    def read_initial_balances(_: DateRange) -> dict[Account, Balance]:
        return initial_balances

    def read_journal_entries(_: DateRange) -> list[JournalEntry]:
        return journal_entries

    program: GeneralLedgerProgram = compile_general_ledger_program(
        read_initial_balances, read_journal_entries
    )
    period = DateRange(start=date(2024, 1, 1), end=date(2024, 12, 31))
    ledger: GeneralLedger = program(period)

    # Verify that the ledger contains the expected accounts and balances
    assert acc_cash in ledger
    assert acc_sales in ledger
    # Cash should be 1200.00 (1000 + 200)
    assert ledger[acc_cash].amount == Decimal("1200.00")
    # Sales should be -200.00
    assert ledger[acc_sales].amount == Decimal("-200.00")


def test_compile_general_ledger_program_boundary_empty_journal(tmp_path):
    """Test that the program handles an empty list of journal entries."""
    acc_cash = _make_account("Cash")
    initial_balances = {acc_cash: _make_balance(Decimal("500.00"))}

    def read_initial_balances(_: DateRange) -> dict[Account, Balance]:
        return initial_balances

    def read_journal_entries(_: DateRange) -> list[JournalEntry]:
        return []

    program: GeneralLedgerProgram = compile_general_ledger_program(
        read_initial_balances, read_journal_entries
    )
    period = DateRange(start=date(2024, 1, 1), end=date(2024, 12, 31))
    ledger: GeneralLedger = program(period)

    # Only the initial balance should be present
    assert ledger == {acc_cash: _make_balance(Decimal("500.00"))}


def test_compile_general_ledger_program_error_in_initial_balances(tmp_path):
    """Test that an exception raised by read_initial_balances propagates."""
    def read_initial_balances(_: DateRange):
        raise RuntimeError("Failed to read balances")

    def read_journal_entries(_: DateRange):
        return []

    program: GeneralLedgerProgram = compile_general_ledger_program(
        read_initial_balances, read_journal_entries
    )
    period = DateRange(start=date(2024, 1, 1), end=date(2024, 12, 31))

    with pytest.raises(RuntimeError, match="Failed to read balances"):
        program(period)
