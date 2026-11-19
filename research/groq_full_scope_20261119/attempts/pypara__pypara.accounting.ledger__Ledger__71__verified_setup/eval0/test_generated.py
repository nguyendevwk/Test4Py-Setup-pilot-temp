import pytest
from decimal import Decimal
from pypara.accounting.ledger import Ledger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import Posting


class DummyDirection:
    """Simple direction mock with a numeric value."""
    def __init__(self, value: int):
        self.value = value


class DummyPosting(Posting):
    """A minimal Posting implementation for testing."""
    def __init__(self, amount: Decimal, direction_value: int):
        self.amount = amount
        self.direction = DummyDirection(direction_value)


def test_ledger_add_increases_balance():
    """Adding a positive posting should increase the ledger balance."""
    account = Account(name="TestAccount")
    ledger = Ledger(account=account, initial=Balance(value=Decimal("100.00")))
    posting = DummyPosting(amount=Decimal("20.00"), direction_value=1)

    entry = ledger.add(posting)

    assert entry.balance == Decimal("120.00")
    assert ledger.entries[-1] is entry
    assert ledger._last_balance == Decimal("120.00")


def test_ledger_add_zero_amount_keeps_balance():
    """Adding a posting with zero amount should leave the balance unchanged."""
    account = Account(name="ZeroAccount")
    ledger = Ledger(account=account, initial=Balance(value=Decimal("50.00")))
    posting = DummyPosting(amount=Decimal("0.00"), direction_value=1)

    entry = ledger.add(posting)

    assert entry.balance == Decimal("50.00")
    assert ledger._last_balance == Decimal("50.00")


def test_ledger_add_missing_attributes_raises():
    """Posting objects missing required attributes should raise AttributeError."""
    account = Account(name="ErrorAccount")
    ledger = Ledger(account=account, initial=Balance(value=Decimal("10.00")))

    class IncompletePosting:
        """Posting lacking amount and direction attributes."""
        pass

    incomplete = IncompletePosting()

    with pytest.raises(AttributeError):
        ledger.add(incomplete)
