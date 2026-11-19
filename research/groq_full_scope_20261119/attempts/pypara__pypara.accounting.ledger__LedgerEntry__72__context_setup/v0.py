import datetime
from decimal import Decimal

import pytest

from pypara.accounting.ledger import LedgerEntry
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.accounts import Account
from pypara.commons.numbers import Quantity


def _make_journal_entry(description: str, postings: list[Posting]) -> JournalEntry:
    """Helper to create a JournalEntry with the given postings."""
    return JournalEntry(description=description, postings=postings)


def _make_posting(account: Account, direction: str, amount: Decimal, date: datetime.date) -> Posting:
    """Helper to create a Posting."""
    return Posting(account=account, direction=direction, amount=amount, date=date)


def test_debit_entry_properties(tmp_path):
    """Test that a debit LedgerEntry exposes correct properties."""
    acct = Account(name="Cash")
    date = datetime.date(2024, 1, 1)
    posting = _make_posting(acct, "debit", Decimal("200.00"), date)
    journal = _make_journal_entry("Test Debit", [posting])
    posting.journal = journal  # attach journal to posting
    balance = Quantity(Decimal("200.00"))
    entry = LedgerEntry(ledger=None, posting=posting, balance=balance)

    assert entry.date == date
    assert entry.description == "Test Debit"
    assert entry.amount == Decimal("200.00")
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Decimal("200.00")
    assert entry.credit is None
    assert entry.balance == balance


def test_credit_entry_properties(tmp_path):
    """Test that a credit LedgerEntry exposes correct properties."""
    acct = Account(name="Revenue")
    date = datetime.date(2024, 2, 2)
    posting = _make_posting(acct, "credit", Decimal("150.00"), date)
    journal = _make_journal_entry("Test Credit", [posting])
    posting.journal = journal
    balance = Quantity(Decimal("150.00"))
    entry = LedgerEntry(ledger=None, posting=posting, balance=balance)

    assert entry.date == date
    assert entry.description == "Test Credit"
    assert entry.amount == Decimal("150.00")
    assert entry.is_debit is False
    assert entry.is_credit is True
    assert entry.debit is None
    assert entry.credit == Decimal("150.00")
    assert entry.balance == balance


def test_cntraccts_list(tmp_path):
    """Test that cntraccts returns the counter accounts for a posting."""
    acct_debit = Account(name="Cash")
    acct_credit = Account(name="Revenue")
    date = datetime.date(2024, 3, 3)
    debit_posting = _make_posting(acct_debit, "debit", Decimal("300.00"), date)
    credit_posting = _make_posting(acct_credit, "credit", Decimal("300.00"), date)
    journal = _make_journal_entry("Test Counter", [debit_posting, credit_posting])
    debit_posting.journal = journal
    credit_posting.journal = journal
    balance = Quantity(Decimal("300.00"))

    debit_entry = LedgerEntry(ledger=None, posting=debit_posting, balance=balance)
    credit_entry = LedgerEntry(ledger=None, posting=credit_posting, balance=balance)

    # For the debit entry, the counter account should be the credit account
    assert debit_entry.cntraccts == [acct_credit]
    # For the credit entry, the counter account should be the debit account
    assert credit_entry.cntraccts == [acct_debit]
