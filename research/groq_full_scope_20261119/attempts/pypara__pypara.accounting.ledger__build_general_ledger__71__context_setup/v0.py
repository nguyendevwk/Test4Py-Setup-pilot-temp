import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import build_general_ledger, GeneralLedger, Ledger, LedgerEntry
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.generic import Balance
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Quantity, Amount


def _make_account(name: str) -> Account:
    """Helper to create a simple Account instance."""
    return Account(name=name)


def _make_posting(account: Account, amount: Decimal, direction: str, date: datetime.date) -> Posting:
    """Helper to create a Posting with a minimal JournalEntry."""
    journal = JournalEntry(
        date=date,
        description=f"{direction} {account.name}",
        postings=[],
    )
    posting = Posting(
        account=account,
        amount=Amount(amount),
        direction=direction,
        journal=journal,
    )
    journal.postings.append(posting)
    return posting


def test_build_general_ledger_basic():
    """Verify that ledger entries are created correctly for a simple period."""
    period = DateRange(since=datetime.date(2023, 1, 1), until=datetime.date(2023, 12, 31))
    acc_cash = _make_account("Cash")
    acc_sales = _make_account("Sales")

    # Opening balances
    initial = {acc_cash: Balance(period.since, Quantity(Decimal("1000.00")))}

    # Journal entries
    entries = [
        JournalEntry(
            date=datetime.date(2023, 3, 15),
            description="Sale",
            postings=[
                Posting(account=acc_sales, amount=Amount(Decimal("200.00")), direction="credit", journal=None),
                Posting(account=acc_cash, amount=Amount(Decimal("200.00")), direction="debit", journal=None),
            ],
        )
    ]

    # Attach journal to postings
    for entry in entries:
        for p in entry.postings:
            p.journal = entry

    ledger = build_general_ledger(period, entries, initial)

    # Check that both accounts have ledgers
    assert acc_cash in ledger.ledgers
    assert acc_sales in ledger.ledgers

    # Cash ledger should have one entry with updated balance
    cash_ledger = ledger.ledgers[acc_cash]
    assert len(cash_ledger.entries) == 1
    cash_entry = cash_ledger.entries[0]
    assert isinstance(cash_entry, LedgerEntry)
    assert cash_entry.balance.value == Decimal("1200.00")
    assert cash_entry.is_debit
    assert cash_entry.debit == Amount(Decimal("200.00"))
    assert cash_entry.credit is None

    # Sales ledger should have one entry with updated balance
    sales_ledger = ledger.ledgers[acc_sales]
    assert len(sales_ledger.entries) == 1
    sales_entry = sales_ledger.entries[0]
    assert sales_entry.balance.value == Decimal("200.00")
    assert sales_entry.is_credit
    assert sales_entry.credit == Amount(Decimal("200.00"))
    assert sales_entry.debit is None


def test_build_general_ledger_boundary_inclusion():
    """Ensure that entries on the boundary dates are included."""
    period = DateRange(since=datetime.date(2023, 1, 1), until=datetime.date(2023, 12, 31))
    acc = _make_account("Revenue")

    initial = {}

    # Entry exactly on the start date
    entry_start = JournalEntry(
        date=period.since,
        description="Start entry",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("50.00")), direction="credit", journal=None),
        ],
    )
    entry_start.postings[0].journal = entry_start

    # Entry exactly on the end date
    entry_end = JournalEntry(
        date=period.until,
        description="End entry",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("75.00")), direction="credit", journal=None),
        ],
    )
    entry_end.postings[0].journal = entry_end

    ledger = build_general_ledger(period, [entry_start, entry_end], initial)

    acc_ledger = ledger.ledgers[acc]
    assert len(acc_ledger.entries) == 2
    assert acc_ledger.entries[0].balance.value == Decimal("50.00")
    assert acc_ledger.entries[1].balance.value == Decimal("125.00")


def test_build_general_ledger_excludes_outside_period():
    """Entries outside the period should not appear in the ledger."""
    period = DateRange(since=datetime.date(2023, 6, 1), until=datetime.date(2023, 6, 30))
    acc = _make_account("Expense")

    initial = {}

    # Entry before period
    entry_before = JournalEntry(
        date=datetime.date(2023, 5, 31),
        description="Before period",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("10.00")), direction="debit", journal=None),
        ],
    )
    entry_before.postings[0].journal = entry_before

    # Entry after period
    entry_after = JournalEntry(
        date=datetime.date(2023, 7, 1),
        description="After period",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("20.00")), direction="debit", journal=None),
        ],
    )
    entry_after.postings[0].journal = entry_after

    ledger = build_general_ledger(period, [entry_before, entry_after], initial)

    # Ledger should not contain the account because no entries in period
    assert acc not in ledger.ledgers
