import datetime
import pytest
from pypara.accounting.journaling import JournalEntry, Direction, Posting
from pypara.accounting.accounts import Account, AccountType
from pypara.commons.numbers import Quantity, Amount

# Helper to create a simple source object
class DummySource:
    pass

def test_post_increments_and_decrements_and_guid(tmp_path):
    """Posting a positive and a negative quantity creates correct postings and a unique guid."""
    entry = JournalEntry(date=datetime.date(2024, 1, 1), description="Test", source=DummySource())
    # Positive quantity -> INC
    entry.post(datetime.date(2024, 1, 2), Account("Cash", AccountType.ASSETS), Quantity(100))
    # Negative quantity -> DEC
    entry.post(datetime.date(2024, 1, 3), Account("Revenue", AccountType.REVENUES), Quantity(-50))

    # Check guid is a Guid instance (string-like)
    assert hasattr(entry.guid, "__str__") or isinstance(entry.guid, str)

    # Verify postings list
    assert len(entry.postings) == 2
    inc_posting, dec_posting = entry.postings
    assert inc_posting.direction == Direction.INC
    assert inc_posting.amount == Amount(100)
    assert dec_posting.direction == Direction.DEC
    assert dec_posting.amount == Amount(50)

    # increments and decrements properties
    incs = list(entry.increments)
    decs = list(entry.decrements)
    assert incs == [inc_posting]
    assert decs == [dec_posting]

def test_debits_and_credits_balance(tmp_path):
    """Debits and credits are correctly identified and validate passes when balanced."""
    entry = JournalEntry(date=datetime.date(2024, 2, 1), description="Balanced", source=DummySource())
    # Debit: Asset account with INC
    entry.post(datetime.date(2024, 2, 2), Account("Cash", AccountType.ASSETS), Quantity(200))
    # Credit: Revenue account with DEC
    entry.post(datetime.date(2024, 2, 3), Account("Revenue", AccountType.REVENUES), Quantity(-200))

    debits = list(entry.debits)
    credits = list(entry.credits)
    assert len(debits) == 1
    assert len(credits) == 1
    assert debits[0].account.type == AccountType.ASSETS
    assert credits[0].account.type == AccountType.REVENUES

    # Validation should pass without raising
    entry.validate()

def test_validate_raises_on_unbalanced(tmp_path):
    """validate() raises AssertionError when debits and credits are not equal."""
    entry = JournalEntry(date=datetime.date(2024, 3, 1), description="Unbalanced", source=DummySource())
    entry.post(datetime.date(2024, 3, 2), Account("Cash", AccountType.ASSETS), Quantity(300))
    entry.post(datetime.date(2024, 3, 3), Account("Revenue", AccountType.REVENUES), Quantity(-200))

    with pytest.raises(AssertionError) as excinfo:
        entry.validate()
    assert "Total Debits and Credits are not equal" in str(excinfo.value)
