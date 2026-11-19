import pytest
from decimal import Decimal
from pypara.accounting.ledger import Ledger
from pypara.accounting.generic import Balance
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import Posting

# Helper minimal direction object
class _Direction:
    def __init__(self, value):
        self.value = value

# Helper minimal posting object
class _Posting:
    def __init__(self, amount, direction_value):
        self.amount = Decimal(amount)
        self.direction = _Direction(direction_value)

def test_ledger_initial_balance():
    """Ledger should expose the initial balance when no entries exist."""
    account = Account(name="Cash")
    initial_balance = Balance(Decimal("1000"))
    ledger = Ledger(account, initial_balance)
    # No entries yet, _last_balance should equal initial value
    assert ledger._last_balance == Decimal("1000")
    # Adding no entries should keep entries list empty
    assert ledger.entries == []

def test_ledger_add_positive_posting():
    """Adding a positive posting updates the balance correctly."""
    account = Account(name="Revenue")
    initial_balance = Balance(Decimal("200"))
    ledger = Ledger(account, initial_balance)
    posting = _Posting(amount="300", direction_value=1)  # credit
    entry = ledger.add(posting)
    # Entry should be appended
    assert ledger.entries[-1] is entry
    # Balance should be initial + amount * direction
    assert entry.balance == Decimal("500")
    # _last_balance property should reflect new balance
    assert ledger._last_balance == Decimal("500")

def test_ledger_add_invalid_posting_raises():
    """Adding a posting lacking required attributes should raise AttributeError."""
    account = Account(name="Expense")
    initial_balance = Balance(Decimal("0"))
    ledger = Ledger(account, initial_balance)
    # Create a posting missing 'amount' attribute
    class BadPosting:
        direction = _Direction(1)
    bad_posting = BadPosting()
    with pytest.raises(AttributeError):
        ledger.add(bad_posting)
