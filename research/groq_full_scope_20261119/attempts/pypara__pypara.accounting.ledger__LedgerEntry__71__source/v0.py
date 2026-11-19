import datetime
from types import SimpleNamespace
import pytest
from pypara.accounting.ledger import LedgerEntry
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import Posting, JournalEntry

# Helper to create a minimal Posting with required attributes
def make_posting(date, amount, direction, account, counter_account):
    # Create a JournalEntry with a description and two postings
    journal = SimpleNamespace(
        description="Test transaction",
        postings=[]
    )
    # Counter posting
    counter_posting = SimpleNamespace(
        account=counter_account,
        direction="credit" if direction == "debit" else "debit",
        amount=-amount,
        date=date,
        journal=journal,
        is_debit=lambda: False,
        is_credit=lambda: False
    )
    # Main posting
    main_posting = SimpleNamespace(
        account=account,
        direction=direction,
        amount=amount,
        date=date,
        journal=journal,
        is_debit=lambda: direction == "debit",
        is_credit=lambda: direction == "credit"
    )
    journal.postings = [main_posting, counter_posting]
    return main_posting

def test_ledger_entry_properties_debit():
    """Test that a debit entry exposes correct properties."""
    acct = Account(name="Cash")
    counter_acct = Account(name="Revenue")
    posting = make_posting(
        date=datetime.date(2023, 1, 15),
        amount=Decimal("100.00"),
        direction="debit",
        account=acct,
        counter_account=counter_acct
    )
    entry = LedgerEntry()
    entry.ledger = None
    entry.posting = posting
    entry.balance = Decimal("100.00")

    assert entry.date == datetime.date(2023, 1, 15)
    assert entry.description == "Test transaction"
    assert entry.amount == Decimal("100.00")
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Decimal("100.00")
    assert entry.credit is None
    assert entry.cntraccts == [counter_acct]

def test_ledger_entry_properties_credit():
    """Test that a credit entry exposes correct properties."""
    acct = Account(name="Revenue")
    counter_acct = Account(name="Cash")
    posting = make_posting(
        date=datetime.date(2023, 2, 20),
        amount=Decimal("200.00"),
        direction="credit",
        account=acct,
        counter_account=counter_acct
    )
    entry = LedgerEntry()
    entry.ledger = None
    entry.posting = posting
    entry.balance = Decimal("200.00")

    assert entry.date == datetime.date(2023, 2, 20)
    assert entry.description == "Test transaction"
    assert entry.amount == Decimal("200.00")
    assert entry.is_debit is False
    assert entry.is_credit is True
    assert entry.debit is None
    assert entry.credit == Decimal("200.00")
    assert entry.cntraccts == [counter_acct]

def test_ledger_entry_counter_accounts_multiple():
    """Test that counter accounts list contains all opposite postings."""
    acct = Account(name="Cash")
    counter_acct1 = Account(name="Revenue")
    counter_acct2 = Account(name="Expense")
    # Create a journal with three postings: one debit, two credits
    journal = SimpleNamespace(
        description="Complex transaction",
        postings=[]
    )
    main_posting = SimpleNamespace(
        account=acct,
        direction="debit",
        amount=Decimal("150.00"),
        date=datetime.date(2023, 3, 10),
        journal=journal,
        is_debit=lambda: True,
        is_credit=lambda: False
    )
    credit1 = SimpleNamespace(
        account=counter_acct1,
        direction="credit",
        amount=Decimal("-100.00"),
        date=datetime.date(2023, 3, 10),
        journal=journal,
        is_debit=lambda: False,
        is_credit=lambda: True
    )
    credit2 = SimpleNamespace(
        account=counter_acct2,
        direction="credit",
        amount=Decimal("-50.00"),
        date=datetime.date(2023, 3, 10),
        journal=journal,
        is_debit=lambda: False,
        is_credit=lambda: True
    )
    journal.postings = [main_posting, credit1, credit2]

    entry = LedgerEntry()
    entry.ledger = None
    entry.posting = main_posting
    entry.balance = Decimal("150.00")

    assert set(entry.cntraccts) == {counter_acct1, counter_acct2}
