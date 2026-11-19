import datetime
import pytest
from decimal import Decimal

from pypara.accounting.ledger import Ledger, LedgerEntry
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.journaling import Direction


def test_ledger_add_and_last_balance(tmp_path):
    """Adding a posting updates the ledger entries and last balance correctly."""
    # Create two accounts
    cash = Account(name="Cash")
    revenue = Account(name="Revenue")

    # Initial ledger with zero balance
    ledger = Ledger(account=cash, initial=Decimal("0.00"))

    # Create a journal entry with a single debit posting
    entry = JournalEntry(
        description="Sale",
        date=datetime.date(2024, 1, 1),
        postings=[
            Posting(account=cash, amount=Decimal("100.00"), direction=Direction.DEBIT),
            Posting(account=revenue, amount=Decimal("100.00"), direction=Direction.CREDIT),
        ],
    )

    # Add the posting to the ledger
    ledger_entry = ledger.add(entry.postings[0])

    # Verify that the ledger now contains one entry
    assert len(ledger.entries) == 1
    assert ledger.entries[0] is ledger_entry

    # The balance should reflect the debit amount
    assert ledger_entry.balance == Decimal("100.00")
    # The last balance property should match the entry's balance
    assert ledger._last_balance == Decimal("100.00")

    # Adding a credit posting should decrease the balance
    credit_entry = ledger.add(entry.postings[1])
    assert credit_entry.balance == Decimal("0.00")
    assert ledger._last_balance == Decimal("0.00")


def test_ledger_entry_properties(tmp_path):
    """LedgerEntry properties expose correct information from the posting."""
    cash = Account(name="Cash")
    revenue = Account(name="Revenue")

    entry = JournalEntry(
        description="Sale",
        date=datetime.date(2024, 2, 1),
        postings=[
            Posting(account=cash, amount=Decimal("200.00"), direction=Direction.DEBIT),
            Posting(account=revenue, amount=Decimal("200.00"), direction=Direction.CREDIT),
        ],
    )

    ledger = Ledger(account=cash, initial=Decimal("0.00"))
    ledger_entry = ledger.add(entry.postings[0])

    # Date, description, amount
    assert ledger_entry.date == datetime.date(2024, 2, 1)
    assert ledger_entry.description == "Sale"
    assert ledger_entry.amount == Decimal("200.00")

    # Counter accounts should list the other posting's account
    assert ledger_entry.cntraccts == [revenue]

    # Debit/credit flags
    assert ledger_entry.is_debit is True
    assert ledger_entry.is_credit is False
    assert ledger_entry.debit == Decimal("200.00")
    assert ledger_entry.credit is None

    # For the credit posting
    credit_entry = ledger.add(entry.postings[1])
    assert credit_entry.is_debit is False
    assert credit_entry.is_credit is True
    assert credit_entry.debit is None
    assert credit_entry.credit == Decimal("200.00")
    assert credit_entry.cntraccts == [cash]


def test_ledger_initial_balance_and_empty_entries(tmp_path):
    """Ledger with no entries should return the initial balance."""
    asset = Account(name="Asset")
    ledger = Ledger(account=asset, initial=Decimal("50.00"))

    # No entries yet
    assert len(ledger.entries) == 0
    # _last_balance should return the initial value
    assert ledger._last_balance == Decimal("50.00")

    # Adding a posting that is a credit reduces the balance
    entry = JournalEntry(
        description="Adjustment",
        date=datetime.date(2024, 3, 1),
        postings=[
            Posting(account=asset, amount=Decimal("20.00"), direction=Direction.CREDIT),
        ],
    )
    ledger.add(entry.postings[0])
    assert ledger._last_balance == Decimal("30.00")
