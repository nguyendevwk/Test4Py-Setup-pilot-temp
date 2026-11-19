import datetime
import pytest
from pypara.accounting.journaling import Posting
from pypara.accounting.accounts import Account, AccountType
from pypara.accounting.journaling import Direction

# Helper to create a minimal JournalEntry placeholder
class DummyJournal:
    pass

def test_posting_debit_logic():
    """Posting with a debit direction should report is_debit True."""
    account = Account(name="Cash", type=AccountType.ASSET)
    posting = Posting(
        journal=DummyJournal(),
        date=datetime.date(2024, 1, 1),
        account=account,
        direction=Direction.DEBIT,
        amount=100.0,
    )
    assert posting.is_debit is True
    assert posting.is_credit is False
    assert posting.amount == 100.0
    assert posting.date == datetime.date(2024, 1, 1)

def test_posting_credit_logic():
    """Posting with a credit direction should report is_credit True."""
    account = Account(name="Revenue", type=AccountType.REVENUE)
    posting = Posting(
        journal=DummyJournal(),
        date=datetime.date(2024, 2, 1),
        account=account,
        direction=Direction.CREDIT,
        amount=200.0,
    )
    assert posting.is_credit is True
    assert posting.is_debit is False
    assert posting.amount == 200.0
    assert posting.date == datetime.date(2024, 2, 1)

def test_posting_zero_amount_boundary():
    """Posting with zero amount should still correctly report debit/credit status."""
    account = Account(name="Liability", type=AccountType.LIABILITY)
    posting = Posting(
        journal=DummyJournal(),
        date=datetime.date(2024, 3, 1),
        account=account,
        direction=Direction.DEBIT,
        amount=0.0,
    )
    assert posting.amount == 0.0
    assert posting.is_debit is True
    assert posting.is_credit is False
