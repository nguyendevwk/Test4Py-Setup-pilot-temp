import pytest
from decimal import Decimal
from pypara.accounting.ledger import Ledger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import Posting, Direction

# Helper to create a minimal posting
def make_posting(amount: Decimal, direction: Direction) -> Posting:
    return Posting(amount=amount, direction=direction)

def test_ledger_initial_balance_and_last_balance():
    """Ledger should expose its initial balance and compute last balance correctly."""
    acc = Account(name="TestAccount")
    init_balance = Balance(value=Decimal("100.00"))
    ledger = Ledger(account=acc, initial=init_balance)
    # No entries yet, last_balance should equal initial
    assert ledger._last_balance == Decimal("100.00")
    # Add a posting that increases balance
    posting = make_posting(Decimal("25.00"), Direction.CREDIT)
    ledger.add(posting)
    # After one entry, last_balance should reflect the change
    assert ledger._last_balance == Decimal("125.00")

def test_ledger_add_multiple_entries_and_balance_updates():
    """Adding multiple entries should accumulate balances correctly."""
    acc = Account(name="MultiEntryAccount")
    init_balance = Balance(value=Decimal("50.00"))
    ledger = Ledger(account=acc, initial=init_balance)
    postings = [
        make_posting(Decimal("10.00"), Direction.CREDIT),
        make_posting(Decimal("5.00"), Direction.DEBIT),
        make_posting(Decimal("20.00"), Direction.CREDIT),
    ]
    expected_balances = [Decimal("60.00"), Decimal("55.00"), Decimal("75.00")]
    for posting, expected in zip(postings, expected_balances):
        entry = ledger.add(posting)
        assert entry.balance == expected
    # Final last_balance should match last entry
    assert ledger._last_balance == Decimal("75.00")
    # Entries list should contain all entries
    assert len(ledger.entries) == 3

def test_ledger_add_invalid_posting_raises():
    """Adding a posting with an unsupported direction should raise an error."""
    acc = Account(name="ErrorAccount")
    init_balance = Balance(value=Decimal("0.00"))
    ledger = Ledger(account=acc, initial=init_balance)
    # Create a posting with an invalid direction (e.g., None)
    with pytest.raises(AttributeError):
        ledger.add(Posting(amount=Decimal("10.00"), direction=None))
