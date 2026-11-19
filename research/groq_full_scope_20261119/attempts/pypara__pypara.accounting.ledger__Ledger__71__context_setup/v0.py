import datetime
import decimal
import pytest
from pypara.accounting.ledger import Ledger, LedgerEntry
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import JournalEntry, Posting, Direction

# Helper to create a minimal journal entry with a single posting
def make_journal_entry(amount: decimal.Decimal, direction: Direction, description: str = "Test") -> JournalEntry:
    # Create a posting that references the journal itself
    posting = Posting(
        journal=None,          # will be set after creation
        account=Account(name="TestAccount"),
        amount=amount,
        direction=direction
    )
    journal = JournalEntry(
        description=description,
        postings=[posting]
    )
    posting.journal = journal
    return journal

def test_ledger_add_updates_entries_and_balance():
    """Adding a posting should create a LedgerEntry and update the ledger balance."""
    account = Account(name="Cash")
    initial_balance = Balance(value=decimal.Decimal("100.00"))
    ledger = Ledger(account=account, initial=initial_balance)

    # Add a debit posting of 50
    journal = make_journal_entry(decimal.Decimal("50.00"), Direction.DEBIT)
    entry = ledger.add(journal.postings[0])

    # The ledger should now contain one entry
    assert len(ledger.entries) == 1
    assert ledger.entries[0] is entry

    # The entry balance should be initial + amount (since debit increases balance)
    expected_balance = decimal.Decimal("150.00")
    assert entry.balance == expected_balance
    assert ledger._last_balance == expected_balance

def test_ledger_last_balance_with_no_entries():
    """When no entries exist, _last_balance should return the initial balance."""
    account = Account(name="Revenue")
    initial_balance = Balance(value=decimal.Decimal("200.00"))
    ledger = Ledger(account=account, initial=initial_balance)

    # No entries added yet
    assert ledger._last_balance == decimal.Decimal("200.00")

def test_ledger_add_multiple_entries_and_balance_sequence():
    """Adding multiple postings should correctly accumulate balances."""
    account = Account(name="Inventory")
    initial_balance = Balance(value=decimal.Decimal("0.00"))
    ledger = Ledger(account=account, initial=initial_balance)

    # First posting: credit 30 (decreases balance)
    journal1 = make_journal_entry(decimal.Decimal("30.00"), Direction.CREDIT)
    entry1 = ledger.add(journal1.postings[0])
    assert entry1.balance == decimal.Decimal("-30.00")

    # Second posting: debit 70 (increases balance)
    journal2 = make_journal_entry(decimal.Decimal("70.00"), Direction.DEBIT)
    entry2 = ledger.add(journal2.postings[0])
    assert entry2.balance == decimal.Decimal("40.00")

    # Third posting: credit 20 (decreases balance)
    journal3 = make_journal_entry(decimal.Decimal("20.00"), Direction.CREDIT)
    entry3 = ledger.add(journal3.postings[0])
    assert entry3.balance == decimal.Decimal("20.00")

    # Final ledger balance should match last entry
    assert ledger._last_balance == decimal.Decimal("20.00")
