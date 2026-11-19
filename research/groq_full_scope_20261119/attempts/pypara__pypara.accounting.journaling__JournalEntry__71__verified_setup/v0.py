import datetime
import pytest
from pypara.accounting.journaling import JournalEntry, Direction
from pypara.accounting.accounts import Account, AccountType
from pypara.commons.numbers import Quantity, Amount


class DummySource:
    """Simple source object for testing."""
    def __repr__(self):
        return "<DummySource>"


def test_post_and_properties(tmp_path):
    """Posting a positive and a negative quantity should create
    increment and decrement postings respectively, and the
    corresponding properties should expose them."""
    entry = JournalEntry(
        date=datetime.date(2024, 1, 1),
        description="Test entry",
        source=DummySource()
    )
    cash = Account("Cash", AccountType.ASSET)
    revenue = Account("Revenue", AccountType.REVENUE)

    # Post a positive quantity (increment)
    entry.post(datetime.date(2024, 1, 1), cash, Quantity(100))
    # Post a negative quantity (decrement)
    entry.post(datetime.date(2024, 1, 1), revenue, Quantity(-50))

    # There should be two postings
    assert len(entry.postings) == 2

    # Check direction of each posting
    inc_postings = list(entry.increments)
    dec_postings = list(entry.decrements)
    assert len(inc_postings) == 1
    assert len(dec_postings) == 1
    assert inc_postings[0].account is cash
    assert dec_postings[0].account is revenue

    # Check debit/credit classification
    debits = list(entry.debits)
    credits = list(entry.credits)
    # In this simple example, both postings are debits because
    # the amount is positive for both (the sign is handled by Direction)
    assert all(p.is_debit for p in debits)
    assert all(p.is_credit for p in credits)


def test_zero_quantity_no_post(tmp_path):
    """Posting a quantity of zero should not create any postings."""
    entry = JournalEntry(
        date=datetime.date(2024, 1, 2),
        description="Zero quantity test",
        source=DummySource()
    )
    bank = Account("Bank", AccountType.ASSET)

    entry.post(datetime.date(2024, 1, 2), bank, Quantity(0))
    assert len(entry.postings) == 0


def test_validate_raises_on_imbalance(tmp_path):
    """validate() should raise an AssertionError when debits and credits
    do not match."""
    entry = JournalEntry(
        date=datetime.date(2024, 1, 3),
        description="Imbalance test",
        source=DummySource()
    )
    asset = Account("Asset", AccountType.ASSET)
    liability = Account("Liability", AccountType.LIABILITY)

    # Post an imbalance: debit 200, credit 100
    entry.post(datetime.date(2024, 1, 3), asset, Quantity(200))
    entry.post(datetime.date(2024, 1, 3), liability, Quantity(-100))

    with pytest.raises(AssertionError) as excinfo:
        entry.validate()
    assert "Total Debits and Credits are not equal" in str(excinfo.value)
