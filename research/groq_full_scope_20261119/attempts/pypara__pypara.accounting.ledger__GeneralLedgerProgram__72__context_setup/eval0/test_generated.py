import datetime
from decimal import Decimal

import pytest

from pypara.accounting.ledger import Ledger, Posting, Account, Quantity, Balance, GeneralLedger
from pypara.commons.numbers import Amount, Quantity as NumQuantity
from pypara.commons.zeitgeist import DateRange


def test_initial_last_balance_returns_initial_value(tmp_path):
    """Ledger with no entries should report its initial balance."""
    acc = Account("Cash")
    init_balance = Balance(Amount(Decimal("100.00")))
    ledger = Ledger(account=acc, initial=init_balance)
    assert ledger._last_balance == NumQuantity(Decimal("100.00"))


def test_add_posting_updates_balance(tmp_path):
    """Adding a posting should create a ledger entry with the correct balance."""
    acc = Account("Revenue")
    init_balance = Balance(Amount(Decimal("0.00")))
    ledger = Ledger(account=acc, initial=init_balance)

    # Posting of +200 to Revenue (direction positive)
    posting = Posting(
        amount=Amount(Decimal("200.00")),
        direction=Posting.Direction.CREDIT,  # assume CREDIT has value +1
        description="Sale",
    )
    entry = ledger.add(posting)

    # The new balance should be 200
    assert entry.balance == NumQuantity(Decimal("200.00"))
    assert ledger.entries[-1] is entry
    assert ledger._last_balance == NumQuantity(Decimal("200.00"))


def test_multiple_postings_accumulate_balance(tmp_path):
    """Sequential postings accumulate correctly in the ledger."""
    acc = Account("Expense")
    init_balance = Balance(Amount(Decimal("50.00")))
    ledger = Ledger(account=acc, initial=init_balance)

    # First posting: -20 (DEBIT)
    posting1 = Posting(
        amount=Amount(Decimal("20.00")),
        direction=Posting.Direction.DEBIT,  # assume DEBIT has value -1
        description="Supplies",
    )
    ledger.add(posting1)

    # Second posting: +30 (CREDIT)
    posting2 = Posting(
        amount=Amount(Decimal("30.00")),
        direction=Posting.Direction.CREDIT,
        description="Refund",
    )
    ledger.add(posting2)

    # Final balance should be 50 - 20 + 30 = 60
    assert ledger._last_balance == NumQuantity(Decimal("60.00"))
