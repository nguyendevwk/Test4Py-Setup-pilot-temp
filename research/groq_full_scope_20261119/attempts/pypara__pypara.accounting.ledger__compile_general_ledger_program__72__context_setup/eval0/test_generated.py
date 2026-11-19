import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import (
    compile_general_ledger_program,
    build_general_ledger,
    Ledger,
    GeneralLedger,
    LedgerEntry,
)
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.accounts import Account
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Quantity, Amount


def _make_account(name: str) -> Account:
    """Utility to create a simple Account instance."""
    return Account(name=name)


def _make_posting(account: Account, amount: Decimal, direction: int, date: datetime.date) -> Posting:
    """Create a Posting with a dummy transaction id."""
    return Posting(
        transaction_id="tx",
        date=date,
        account=account,
        amount=Amount(amount),
        direction=direction,
    )


def _make_journal_entry(date: datetime.date, postings: list[Posting]) -> JournalEntry:
    return JournalEntry(transaction_id="tx", date=date, postings=postings)


def test_compile_general_ledger_program_normal(tmp_path):
    """Normal scenario: initial balances and journal entries are processed correctly."""
    # Setup period
    since = datetime.date(2023, 1, 1)
    until = datetime.date(2023, 12, 31)
    period = DateRange(since=since, until=until)

    # Accounts
    acc_cash = _make_account("Cash")
    acc_sales = _make_account("Sales")

    # Initial balances
    initial_balances = {acc_cash: Ledger(acc_cash, Balance(since, Quantity(Decimal("1000.00"))))}

    # Journal entries
    posting1 = _make_posting(acc_cash, Decimal("-200.00"), 1, datetime.date(2023, 6, 15))
    posting2 = _make_posting(acc_sales, Decimal("200.00"), -1, datetime.date(2023, 6, 15))
    journal_entries = [_make_journal_entry(datetime.date(2023, 6, 15), [posting1, posting2])]

    # Read functions
    def read_initial_balances(p: DateRange):
        assert p == period
        return initial_balances

    def read_journal_entries(p: DateRange):
        assert p == period
        return journal_entries

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)
    gl = program(period)

    # Assertions
    assert isinstance(gl, GeneralLedger)
    assert gl.period == period
    assert acc_cash in gl.ledgers
    assert acc_sales in gl.ledgers

    cash_ledger = gl.ledgers[acc_cash]
    sales_ledger = gl.ledgers[acc_sales]

    # Cash ledger should have initial balance and one posting
    assert len(cash_ledger.entries) == 1
    assert cash_ledger.entries[0].balance == Quantity(Decimal("800.00"))
    # Sales ledger should have initial zero and one posting
    assert len(sales_ledger.entries) == 1
    assert sales_ledger.entries[0].balance == Quantity(Decimal("200.00"))


def test_compile_general_ledger_program_boundary(tmp_path):
    """Boundary scenario: postings outside the period are ignored."""
    since = datetime.date(2023, 1, 1)
    until = datetime.date(2023, 12, 31)
    period = DateRange(since=since, until=until)

    acc = _make_account("Revenue")

    initial_balances = {acc: Ledger(acc, Balance(since, Quantity(Decimal("0.00"))))}

    # Posting before period
    posting_before = _make_posting(acc, Decimal("100.00"), -1, datetime.date(2022, 12, 31))
    # Posting after period
    posting_after = _make_posting(acc, Decimal("200.00"), -1, datetime.date(2024, 1, 1))
    # Posting inside period
    posting_inside = _make_posting(acc, Decimal("300.00"), -1, datetime.date(2023, 6, 1))

    journal_entries = [
        _make_journal_entry(posting_before.date, [posting_before]),
        _make_journal_entry(posting_inside.date, [posting_inside]),
        _make_journal_entry(posting_after.date, [posting_after]),
    ]

    def read_initial_balances(p: DateRange):
        return initial_balances

    def read_journal_entries(p: DateRange):
        return journal_entries

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)
    gl = program(period)

    ledger = gl.ledgers[acc]
    # Only the inside posting should be applied
    assert len(ledger.entries) == 1
    assert ledger.entries[0].balance == Quantity(Decimal("300.00"))


def test_compile_general_ledger_program_missing_initial(tmp_path):
    """Error scenario: posting to an account without initial balance creates a new ledger."""
    since = datetime.date(2023, 1, 1)
    until = datetime.date(2023, 12, 31)
    period = DateRange(since=since, until=until)

    acc_new = _make_account("NewAccount")

    initial_balances = {}  # No initial balances

    posting = _make_posting(acc_new, Decimal("50.00"), 1, datetime.date(2023, 3, 15))
    journal_entries = [_make_journal_entry(posting.date, [posting])]

    def read_initial_balances(p: DateRange):
        return initial_balances

    def read_journal_entries(p: DateRange):
        return journal_entries

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)
    gl = program(period)

    ledger = gl.ledgers[acc_new]
    # Ledger should be created with zero initial balance
    assert ledger.initial.value == Quantity(Decimal("0.00"))
    assert len(ledger.entries) == 1
    assert ledger.entries[0].balance == Quantity(Decimal("50.00"))
