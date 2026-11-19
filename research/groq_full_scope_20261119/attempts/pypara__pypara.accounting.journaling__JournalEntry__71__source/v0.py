import datetime
import pytest
from pypara.accounting.journaling import JournalEntry, Direction
from pypara.accounting.accounts import Account, AccountType

# Helper source object (could be any type)
class DummySource:
    pass

def test_posting_increments_and_decrements():
    """Posting a positive quantity creates an increment posting,
    a negative quantity creates a decrement posting."""
    entry = JournalEntry[DummySource]()
    entry.source = DummySource()
    account = Account(name="Cash", type=AccountType.ASSET)

    # Positive quantity -> increment
    entry.post(datetime.date(2024, 1, 1), account, 100)
    inc_postings = list(entry.increments)
    assert len(inc_postings) == 1
    inc = inc_postings[0]
    assert inc.direction == Direction.INC
    assert inc.amount == 100
    assert inc.is_debit  # by default, increments are debits

    # Negative quantity -> decrement
    entry.post(datetime.date(2024, 1, 2), account, -50)
    dec_postings = list(entry.decrements)
    assert len(dec_postings) == 1
    dec = dec_postings[0]
    assert dec.direction == Direction.DEC
    assert dec.amount == 50
    assert dec.is_credit  # decrements are credits

def test_zero_quantity_no_posting():
    """Posting a zero quantity should not create any posting."""
    entry = JournalEntry[DummySource]()
    entry.source = DummySource()
    account = Account(name="Revenue", type=AccountType.REVENUE)

    entry.post(datetime.date(2024, 1, 3), account, 0)
    assert len(entry.postings) == 0

def test_validate_balanced_and_unbalanced():
    """validate() passes when debits equal credits, raises otherwise."""
    entry = JournalEntry[DummySource]()
    entry.source = DummySource()
    acc_debit = Account(name="Cash", type=AccountType.ASSET)
    acc_credit = Account(name="Revenue", type=AccountType.REVENUE)

    # Balanced entry: 200 debit, 200 credit
    entry.post(datetime.date(2024, 1, 4), acc_debit, 200)   # debit
    entry.post(datetime.date(2024, 1, 4), acc_credit, -200) # credit
    # Should not raise
    entry.validate()

    # Unbalanced entry: 300 debit, 200 credit
    entry2 = JournalEntry[DummySource]()
    entry2.source = DummySource()
    entry2.post(datetime.date(2024, 1, 5), acc_debit, 300)
    entry2.post(datetime.date(2024, 1, 5), acc_credit, -200)
    with pytest.raises(AssertionError) as excinfo:
        entry2.validate()
    assert "Total Debits and Credits are not equal" in str(excinfo.value)
