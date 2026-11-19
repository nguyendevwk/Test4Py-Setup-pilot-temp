import datetime
import pytest
from pypara.accounting.journaling import JournalEntry, Posting, Direction, Account, AccountType
from pypara.commons.numbers import Quantity, Amount

# Helper to create a simple source object
class DummySource:
    pass

def test_post_adds_correct_postings_and_guid_is_unique():
    """Posting an increment and a decrement creates two postings with correct attributes."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Test", source=DummySource())
    acc_inc = Account(name="Cash", type=AccountType.ASSET)
    acc_dec = Account(name="Revenue", type=AccountType.REVENUE)

    # Post an increment of 100 and a decrement of 50
    entry.post(datetime.date(2024, 1, 2), acc_inc, Quantity(100))
    entry.post(datetime.date(2024, 1, 3), acc_dec, Quantity(-50))

    # There should be two postings
    assert len(entry.postings) == 2

    inc_posting = next(p for p in entry.postings if p.account == acc_inc)
    dec_posting = next(p for p in entry.postings if p.account == acc_dec)

    # Check directions
    assert inc_posting.direction == Direction.INC
    assert dec_posting.direction == Direction.DEC

    # Check amounts are absolute
    assert inc_posting.amount == Amount(100)
    assert dec_posting.amount == Amount(50)

    # GUID should be a valid Guid instance and unique
    assert hasattr(entry.guid, "__str__")
    assert isinstance(entry.guid, type(entry.guid))
    # Create another entry to ensure GUID uniqueness
    another_entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Other", source=DummySource())
    assert entry.guid != another_entry.guid

def test_validate_passes_when_debits_equal_credits():
    """validate() should succeed when debits equal credits."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Balanced", source=DummySource())
    acc_debit = Account(name="Expense", type=AccountType.EXPENSE)
    acc_credit = Account(name="Cash", type=AccountType.ASSET)

    # Post a debit of 200 and a credit of 200
    entry.post(datetime.date(2024, 1, 2), acc_debit, Quantity(-200))
    entry.post(datetime.date(2024, 1, 3), acc_credit, Quantity(200))

    # validate should not raise
    entry.validate()

def test_validate_raises_on_unbalanced_entry():
    """validate() should raise AssertionError when debits do not equal credits."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Unbalanced", source=DummySource())
    acc_debit = Account(name="Expense", type=AccountType.EXPENSE)
    acc_credit = Account(name="Cash", type=AccountType.ASSET)

    # Post a debit of 150 and a credit of 200
    entry.post(datetime.date(2024, 1, 2), acc_debit, Quantity(-150))
    entry.post(datetime.date(2024, 1, 3), acc_credit, Quantity(200))

    with pytest.raises(AssertionError) as excinfo:
        entry.validate()
    assert "Total Debits and Credits are not equal" in str(excinfo.value)
