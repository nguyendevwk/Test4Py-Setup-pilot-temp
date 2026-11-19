import datetime
import pytest
from decimal import Decimal

from pypara.accounting.ledger import Ledger, GeneralLedger, Account, Posting, Quantity, Balance
from pypara.commons.numbers import Amount, Quantity as Qty
from pypara.commons.zeitgeist import DateRange


def test_ledger_initial_balance_and_entries(tmp_path):
    """Ledger should start with the given initial balance and no entries."""
    acc = Account("Cash")
    init_balance = Balance(Amount(Decimal("100.00")))
    ledger = Ledger(account=acc, initial=init_balance)
    assert ledger.account is acc
    assert ledger.initial == init_balance
    assert ledger.entries == []


def test_ledger_add_posting_updates_balance(tmp_path):
    """Adding a posting should create a ledger entry with the correct balance."""
    acc = Account("Revenue")
    init_balance = Balance(Amount(Decimal("0.00")))
    ledger = Ledger(account=acc, initial=init_balance)

    # Create a posting that increases the balance by 50
    posting = Posting(
        amount=Amount(Decimal("50.00")),
        direction=Posting.Direction.CREDIT,
        description="Sale",
        date=datetime.date.today(),
    )
    entry = ledger.add(posting)

    # The entry should be appended to the ledger
    assert ledger.entries[-1] is entry
    # The balance should reflect the posting
    expected_balance = Qty(init_balance.value + posting.amount * posting.direction.value)
    assert entry.balance == expected_balance
    # The ledger's last balance property should match
    assert ledger._last_balance == expected_balance


def test_ledger_last_balance_without_entries(tmp_path):
    """_last_balance should return the initial value when no entries exist."""
    acc = Account("Expenses")
    init_balance = Balance(Amount(Decimal("200.00")))
    ledger = Ledger(account=acc, initial=init_balance)
    assert ledger._last_balance == init_balance.value
