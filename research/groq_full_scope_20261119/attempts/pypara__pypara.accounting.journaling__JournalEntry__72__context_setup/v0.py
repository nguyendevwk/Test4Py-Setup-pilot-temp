import datetime
import pytest
from pypara.accounting.journaling import JournalEntry, Posting, Direction
from pypara.accounting.accounts import Account, AccountType

# Helper account class for testing
class DummyAccount(Account):
    def __init__(self, name: str, acc_type: AccountType):
        self.name = name
        self.type = acc_type

def test_post_and_properties():
    """Posting increments/decrements and property filters work correctly."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Test", source="src")
    acc_asset = DummyAccount("Cash", AccountType.ASSETS)
    acc_rev = DummyAccount("Sales", AccountType.REVENUES)

    # Post positive quantity (increment) to asset account
    entry.post(datetime.date(2024, 1, 2), acc_asset, 100)
    # Post negative quantity (decrement) to revenue account
    entry.post(datetime.date(2024, 1, 3), acc_rev, -50)

    # There should be two postings
    assert len(entry.postings) == 2

    inc_postings = list(entry.increments)
    dec_postings = list(entry.decrements)
    assert len(inc_postings) == 1
    assert len(dec_postings) == 1
    assert inc_postings[0].account is acc_asset
    assert dec_postings[0].account is acc_rev

    # Debit/credit classification
    debits = list(entry.debits)
    credits = list(entry.credits)
    # Asset increment is a debit, revenue decrement is a credit
    assert debits[0].account is acc_asset
    assert credits[0].account is acc_rev

def test_zero_quantity_no_posting():
    """Posting with zero quantity should not create a posting."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Zero test", source="src")
    acc_exp = DummyAccount("Expense", AccountType.EXPENSES)
    entry.post(datetime.date(2024, 1, 2), acc_exp, 0)
    assert len(entry.postings) == 0

def test_validate_raises_on_imbalance():
    """validate should raise AssertionError when debits and credits differ."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Imbalance", source="src")
    acc_asset = DummyAccount("Cash", AccountType.ASSETS)
    acc_rev = DummyAccount("Sales", AccountType.REVENUES)

    # Post 100 to asset (debit) and 50 to revenue (credit)
    entry.post(datetime.date(2024, 1, 2), acc_asset, 100)
    entry.post(datetime.date(2024, 1, 3), acc_rev, -50)

    with pytest.raises(AssertionError, match="Total Debits and Credits are not equal"):
        entry.validate()
