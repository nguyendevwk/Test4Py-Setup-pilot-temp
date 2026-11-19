import datetime
from types import SimpleNamespace
from decimal import Decimal

import pytest

from pypara.accounting.ledger import LedgerEntry
from pypara.accounting.accounts import Account
from pypara.commons.numbers import Amount, Quantity


def make_posting(amount, direction, date, description, counter_accounts):
    """Create a minimal posting object with the attributes required by LedgerEntry."""
    # Create a dummy journal entry with a list of postings
    postings = []
    for acct, dir_ in counter_accounts:
        postings.append(SimpleNamespace(account=acct, direction=dir_))
    journal = SimpleNamespace(
        description=description,
        postings=postings,
    )
    return SimpleNamespace(
        date=date,
        journal=journal,
        amount=amount,
        direction=direction,
        is_debit=(direction == "debit"),
        is_credit=(direction == "credit"),
    )


def test_ledger_entry_basic_properties():
    """Test that LedgerEntry exposes the correct basic properties."""
    date = datetime.date(2023, 1, 15)
    amount = Amount(Decimal("100.00"))
    acct = Account("Cash")
    posting = make_posting(amount, "debit", date, "Test transaction", [(acct, "credit")])
    entry = LedgerEntry(ledger=None, posting=posting, balance=Quantity(Decimal("100.00")))

    assert entry.date == date
    assert entry.description == "Test transaction"
    assert entry.amount == amount
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == amount
    assert entry.credit is None
    assert entry.cntraccts == [acct]


def test_ledger_entry_credit_and_counter_accounts():
    """Test that a credit entry correctly identifies counter accounts."""
    date = datetime.date(2023, 2, 20)
    amount = Amount(Decimal("50.00"))
    acct1 = Account("Revenue")
    acct2 = Account("Cash")
    posting = make_posting(amount, "credit", date, "Sale", [(acct1, "debit"), (acct2, "debit")])
    entry = LedgerEntry(ledger=None, posting=posting, balance=Quantity(Decimal("-50.00")))

    assert entry.is_debit is False
    assert entry.is_credit is True
    assert entry.debit is None
    assert entry.credit == amount
    # Counter accounts are those with direction different from the posting's direction
    assert set(entry.cntraccts) == {acct1, acct2}


def test_ledger_entry_multiple_counter_accounts_and_balance():
    """Test that multiple counter accounts are returned and balance is stored."""
    date = datetime.date(2023, 3, 5)
    amount = Amount(Decimal("200.00"))
    acct1 = Account("Accounts Receivable")
    acct2 = Account("Sales")
    acct3 = Account("Tax Payable")
    posting = make_posting(
        amount,
        "debit",
        date,
        "Invoice issued",
        [(acct1, "credit"), (acct2, "credit"), (acct3, "credit")],
    )
    balance = Quantity(Decimal("200.00"))
    entry = LedgerEntry(ledger=None, posting=posting, balance=balance)

    assert entry.balance == balance
    assert set(entry.cntraccts) == {acct1, acct2, acct3}
    assert entry.debit == amount
    assert entry.credit is None
