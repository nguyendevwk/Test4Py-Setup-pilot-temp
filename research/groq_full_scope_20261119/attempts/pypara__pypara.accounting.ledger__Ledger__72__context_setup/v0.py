import datetime
import pytest
from decimal import Decimal

from pypara.accounting.ledger import Ledger, LedgerEntry
from pypara.accounting.generic import Balance
from pypara.accounting.accounts import Account


# Minimal stubs for the required objects
class DummyDirection:
    def __init__(self, value, is_debit, is_credit):
        self.value = value
        self.is_debit = is_debit
        self.is_credit = is_credit


class DummyJournal:
    def __init__(self, description, postings):
        self.description = description
        self.postings = postings


class DummyPosting:
    def __init__(self, amount, direction, date, journal):
        self.amount = amount
        self.direction = direction
        self.date = date
        self.journal = journal

    @property
    def is_debit(self):
        return self.direction.is_debit

    @property
    def is_credit(self):
        return self.direction.is_credit


def test_ledger_add_debit_updates_balance():
    """Adding a debit posting should increase the balance."""
    account = Account("Cash")
    ledger = Ledger(account, Balance(Decimal("100.00")))
    debit_dir = DummyDirection(value=1, is_debit=True, is_credit=False)
    journal = DummyJournal("Purchase", postings=[])
    posting = DummyPosting(amount=Decimal("25.00"), direction=debit_dir,
                           date=datetime.date.today(), journal=journal)

    entry = ledger.add(posting)

    assert isinstance(entry, LedgerEntry)
    assert entry.balance == Decimal("125.00")
    assert ledger.entries[-1] is entry
    assert ledger._last_balance == Decimal("125.00")


def test_ledger_add_zero_amount_no_change():
    """Adding a posting with zero amount should leave balance unchanged."""
    account = Account("Revenue")
    ledger = Ledger(account, Balance(Decimal("200.00")))
    credit_dir = DummyDirection(value=-1, is_debit=False, is_credit=True)
    journal = DummyJournal("Sale", postings=[])
    posting = DummyPosting(amount=Decimal("0.00"), direction=credit_dir,
                           date=datetime.date.today(), journal=journal)

    entry = ledger.add(posting)

    assert entry.balance == Decimal("200.00")
    assert ledger._last_balance == Decimal("200.00")
    assert ledger.entries[-1] is entry


def test_ledger_add_invalid_posting_raises():
    """Adding a posting missing required attributes should raise an exception."""
    account = Account("Expense")
    ledger = Ledger(account, Balance(Decimal("50.00")))
    # Posting with None amount will cause arithmetic error
    debit_dir = DummyDirection(value=1, is_debit=True, is_credit=False)
    journal = DummyJournal("Refund", postings=[])
    posting = DummyPosting(amount=None, direction=debit_dir,
                           date=datetime.date.today(), journal=journal)

    with pytest.raises(TypeError):
        ledger.add(posting)
