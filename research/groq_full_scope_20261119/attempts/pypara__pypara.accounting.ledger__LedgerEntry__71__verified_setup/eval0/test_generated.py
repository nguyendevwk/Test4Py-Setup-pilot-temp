import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import LedgerEntry
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.commons.numbers import Amount, Quantity
from pypara.commons.zeitgeist import DateRange

# Helper to create a simple ledger with a single posting
def make_ledger_entry(date, description, amount, direction, counter_account_name):
    # Create accounts
    main_account = Account(name="Main")
    counter_account = Account(name=counter_account_name)

    # Create posting
    posting = Posting(
        account=main_account,
        amount=Amount(amount),
        direction=direction,
        date=date,
    )

    # Create journal entry containing the posting and the counter posting
    counter_posting = Posting(
        account=counter_account,
        amount=Amount(amount),
        direction=direction.opposite(),
        date=date,
    )
    journal = JournalEntry(
        description=description,
        postings=[posting, counter_posting],
    )

    # Attach posting to journal
    posting.journal = journal
    counter_posting.journal = journal

    # Create ledger and balance
    ledger = Balance()
    ledger.add_entry(posting)

    # Create LedgerEntry
    return LedgerEntry(ledger=ledger, posting=posting, balance=ledger.balance)

def test_debit_entry_properties():
    date = datetime.date(2023, 1, 15)
    entry = make_ledger_entry(
        date=date,
        description="Test Debit",
        amount=Decimal("100.00"),
        direction=Posting.Direction.DEBIT,
        counter_account_name="Cash",
    )

    assert entry.date == date
    assert entry.description == "Test Debit"
    assert entry.amount == Amount(Decimal("100.00"))
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Amount(Decimal("100.00"))
    assert entry.credit is None
    # Counter accounts should include the counter account only
    assert len(entry.cntraccts) == 1
    assert entry.cntraccts[0].name == "Cash"

def test_credit_entry_properties():
    date = datetime.date(2023, 2, 20)
    entry = make_ledger_entry(
        date=date,
        description="Test Credit",
        amount=Decimal("50.00"),
        direction=Posting.Direction.CREDIT,
        counter_account_name="Revenue",
    )

    assert entry.date == date
    assert entry.description == "Test Credit"
    assert entry.amount == Amount(Decimal("50.00"))
    assert entry.is_debit is False
    assert entry.is_credit is True
    assert entry.debit is None
    assert entry.credit == Amount(Decimal("50.00"))
    # Counter accounts should include the counter account only
    assert len(entry.cntraccts) == 1
    assert entry.cntraccts[0].name == "Revenue"

def test_zero_amount_entry():
    date = datetime.date(2023, 3, 10)
    entry = make_ledger_entry(
        date=date,
        description="Zero Amount",
        amount=Decimal("0.00"),
        direction=Posting.Direction.DEBIT,
        counter_account_name="ZeroAccount",
    )

    # Even with zero amount, debit/credit flags are based on direction
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Amount(Decimal("0.00"))
    assert entry.credit is None
    # Counter accounts should still be present
    assert len(entry.cntraccts) == 1
    assert entry.cntraccts[0].name == "ZeroAccount"
