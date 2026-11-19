import datetime
from decimal import Decimal
import pytest

# Import the target class
from pypara.accounting.ledger import LedgerEntry

# Minimal stand‑in classes that satisfy the attributes used by LedgerEntry
class DummyJournal:
    def __init__(self, description, postings):
        self.description = description
        self.postings = postings

class DummyPosting:
    def __init__(self, date, amount, direction, account, journal):
        self.date = date
        self.amount = amount
        self.direction = direction
        self.account = account
        self.journal = journal

    @property
    def is_debit(self):
        return self.direction == "debit"

    @property
    def is_credit(self):
        return self.direction == "credit"

class DummyAccount:
    def __init__(self, name):
        self.name = name

# Dummy ledger placeholder – its type is irrelevant for the tests
class DummyLedger:
    pass

def test_debit_entry_properties(tmp_path):
    """Verify that a debit entry exposes correct attributes."""
    date = datetime.date(2023, 1, 15)
    amount = Decimal("100.00")
    account = DummyAccount("Cash")
    counter_account = DummyAccount("Revenue")
    journal = DummyJournal("Sale", [])
    posting = DummyPosting(date, amount, "debit", account, journal)
    # Add counter posting to journal for cntraccts
    counter_posting = DummyPosting(date, amount, "credit", counter_account, journal)
    journal.postings.extend([posting, counter_posting])

    entry = LedgerEntry(DummyLedger(), posting, amount)

    assert entry.date == date
    assert entry.description == "Sale"
    assert entry.amount == amount
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == amount
    assert entry.credit is None
    assert entry.cntraccts == [counter_account]

def test_credit_entry_properties(tmp_path):
    """Verify that a credit entry exposes correct attributes."""
    date = datetime.date(2023, 2, 20)
    amount = Decimal("200.00")
    account = DummyAccount("Accounts Receivable")
    counter_account = DummyAccount("Sales")
    journal = DummyJournal("Invoice", [])
    posting = DummyPosting(date, amount, "credit", account, journal)
    counter_posting = DummyPosting(date, amount, "debit", counter_account, journal)
    journal.postings.extend([posting, counter_posting])

    entry = LedgerEntry(DummyLedger(), posting, amount)

    assert entry.date == date
    assert entry.description == "Invoice"
    assert entry.amount == amount
    assert entry.is_debit is False
    assert entry.is_credit is True
    assert entry.credit == amount
    assert entry.debit is None
    assert entry.cntraccts == [counter_account]

def test_zero_amount_entry(tmp_path):
    """Zero amount should yield None for debit and credit."""
    date = datetime.date(2023, 3, 5)
    amount = Decimal("0.00")
    account = DummyAccount("Misc")
    journal = DummyJournal("Zero", [])
    posting = DummyPosting(date, amount, "debit", account, journal)

    entry = LedgerEntry(DummyLedger(), posting, amount)

    # Even though direction is debit, amount zero means no real debit/credit
    assert entry.debit is None
    assert entry.credit is None
    # Properties still reflect the posting direction
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.amount == amount
