import datetime
import pytest
from pypara.accounting.journaling import JournalEntry, Direction, Posting
from pypara.accounting.accounts import Account, AccountType

# Helper source object (any type is fine)
class DummySource:
    pass

def test_posting_increments_and_decrements(tmp_path):
    entry = JournalEntry[DummySource]()
    entry.source = DummySource()
    entry.date = datetime.date.today()
    entry.description = "Test entry"

    # Create two accounts
    acc_inc = Account("Cash", AccountType.ASSET)
    acc_dec = Account("Revenue", AccountType.REVENUE)

    # Post positive quantity (increment)
    entry.post(entry.date, acc_inc, 100)
    # Post negative quantity (decrement)
    entry.post(entry.date, acc_dec, -50)

    # Verify postings count
    assert len(entry.postings) == 2

    # Verify increments and decrements
    inc_postings = list(entry.increments)
    dec_postings = list(entry.decrements)
    assert len(inc_postings) == 1
    assert len(dec_postings) == 1
    assert inc_postings[0].account == acc_inc
    assert dec_postings[0].account == acc_dec

    # Verify amounts are absolute
    assert inc_postings[0].amount == 100
    assert dec_postings[0].amount == 50

def test_zero_quantity_not_posted(tmp_path):
    entry = JournalEntry[DummySource]()
    entry.source = DummySource()
    entry.date = datetime.date.today()
    entry.description = "Zero quantity test"

    acc = Account("Bank", AccountType.ASSET)

    # Post zero quantity
    entry.post(entry.date, acc, 0)

    # No postings should be added
    assert len(entry.postings) == 0

def test_validate_raises_on_imbalance(tmp_path):
    entry = JournalEntry[DummySource]()
    entry.source = DummySource()
    entry.date = datetime.date.today()
    entry.description = "Imbalance test"

    acc_debit = Account("Expense", AccountType.EXPENSE)
    acc_credit = Account("Cash", AccountType.ASSET)

    # Post debit of 200
    entry.post(entry.date, acc_debit, 200)
    # Post credit of 100 (imbalance)
    entry.post(entry.date, acc_credit, -100)

    # Validate should raise AssertionError due to imbalance
    with pytest.raises(AssertionError) as excinfo:
        entry.validate()
    assert "Total Debits and Credits are not equal" in str(excinfo.value)
