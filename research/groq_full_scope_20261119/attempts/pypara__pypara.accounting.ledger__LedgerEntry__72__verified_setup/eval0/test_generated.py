import datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest

from pypara.accounting.ledger import LedgerEntry
from pypara.commons.numbers import Quantity
from pypara.accounting.accounts import Account


def _make_journal(description: str, postings: list):
    """Create a simple journal object with required attributes."""
    return SimpleNamespace(description=description, postings=postings)


def _make_posting(
    account: Account,
    direction: str,
    amount: Decimal,
    date: datetime.date,
    journal,
):
    """Create a simple posting object with required attributes."""
    is_debit = direction.lower() == "debit"
    is_credit = direction.lower() == "credit"
    return SimpleNamespace(
        account=account,
        direction=direction,
        amount=amount,
        date=date,
        journal=journal,
        is_debit=is_debit,
        is_credit=is_credit,
    )


def test_debit_entry_properties(tmp_path):
    """Test that a debit ledger entry exposes correct attributes."""
    acc_debit = Account(name="Cash")
    acc_credit = Account(name="Revenue")
    date = datetime.date(2024, 1, 1)

    # Create postings
    debit_posting = _make_posting(
        account=acc_debit,
        direction="debit",
        amount=Decimal("200.00"),
        date=date,
        journal=None,
    )
    credit_posting = _make_posting(
        account=acc_credit,
        direction="credit",
        amount=Decimal("200.00"),
        date=date,
        journal=None,
    )

    # Create journal linking postings
    journal = _make_journal("Sale", [debit_posting, credit_posting])
    debit_posting.journal = journal
    credit_posting.journal = journal

    entry = LedgerEntry(ledger=None, posting=debit_posting, balance=Quantity(Decimal("200.00")))

    assert entry.date == date
    assert entry.description == "Sale"
    assert entry.amount == Decimal("200.00")
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Decimal("200.00")
    assert entry.credit is None
    # Counter accounts should contain the credit account only
    assert entry.cntraccts == [acc_credit]


def test_credit_entry_properties(tmp_path):
    """Test that a credit ledger entry exposes correct attributes."""
    acc_debit = Account(name="Expense")
    acc_credit = Account(name="Cash")
    date = datetime.date(2024, 2, 15)

    debit_posting = _make_posting(
        account=acc_debit,
        direction="debit",
        amount=Decimal("50.00"),
        date=date,
        journal=None,
    )
    credit_posting = _make_posting(
        account=acc_credit,
        direction="credit",
        amount=Decimal("50.00"),
        date=date,
        journal=None,
    )

    journal = _make_journal("Purchase", [debit_posting, credit_posting])
    debit_posting.journal = journal
    credit_posting.journal = journal

    entry = LedgerEntry(ledger=None, posting=credit_posting, balance=Quantity(Decimal("150.00")))

    assert entry.date == date
    assert entry.description == "Purchase"
    assert entry.amount == Decimal("50.00")
    assert entry.is_debit is False
    assert entry.is_credit is True
    assert entry.debit is None
    assert entry.credit == Decimal("50.00")
    # Counter accounts should contain the debit account only
    assert entry.cntraccts == [acc_debit]


def test_zero_amount_entry(tmp_path):
    """Test that a zero‑amount entry still reports debit/credit correctly."""
    acc_debit = Account(name="ZeroDebit")
    acc_credit = Account(name="ZeroCredit")
    date = datetime.date(2024, 3, 10)

    zero_posting = _make_posting(
        account=acc_debit,
        direction="debit",
        amount=Decimal("0.00"),
        date=date,
        journal=None,
    )
    other_posting = _make_posting(
        account=acc_credit,
        direction="credit",
        amount=Decimal("0.00"),
        date=date,
        journal=None,
    )

    journal = _make_journal("ZeroTransaction", [zero_posting, other_posting])
    zero_posting.journal = journal
    other_posting.journal = journal

    entry = LedgerEntry(ledger=None, posting=zero_posting, balance=Quantity(Decimal("0.00")))

    assert entry.amount == Decimal("0.00")
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Decimal("0.00")
    assert entry.credit is None
    assert entry.cntraccts == [acc_credit]
