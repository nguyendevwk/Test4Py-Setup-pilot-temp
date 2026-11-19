import datetime
import pytest
from pypara.accounting.journaling import Posting, Direction
from pypara.accounting.accounts import AccountType
from pypara.commons.numbers import Amount

# Simple stand‑in for the Account class used by Posting.
class DummyAccount:
    def __init__(self, account_type: AccountType):
        self.type = account_type

# A minimal JournalEntry placeholder required by Posting.
class DummyJournalEntry:
    pass

def test_posting_debit_inc_assets():
    """Posting with INC direction on an ASSETS account should be a debit."""
    account = DummyAccount(AccountType.ASSETS)
    posting = Posting(
        journal=DummyJournalEntry(),
        date=datetime.date.today(),
        account=account,
        direction=Direction.INC,
        amount=Amount(100)
    )
    assert posting.is_debit is True
    assert posting.is_credit is False

def test_posting_credit_dec_revenues():
    """Posting with DEC direction on a REVENUES account should be a credit."""
    account = DummyAccount(AccountType.REVENUES)
    posting = Posting(
        journal=DummyJournalEntry(),
        date=datetime.date.today(),
        account=account,
        direction=Direction.DEC,
        amount=Amount(200)
    )
    assert posting.is_debit is False
    assert posting.is_credit is True

def test_posting_debit_dec_expenses():
    """Posting with DEC direction on an EXPENSES account should be a debit."""
    account = DummyAccount(AccountType.EXPENSES)
    posting = Posting(
        journal=DummyJournalEntry(),
        date=datetime.date.today(),
        account=account,
        direction=Direction.DEC,
        amount=Amount(50)
    )
    assert posting.is_debit is True
    assert posting.is_credit is False
