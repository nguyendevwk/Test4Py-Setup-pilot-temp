import datetime
from decimal import Decimal
import pytest
from pypara.accounting.ledger import Ledger, LedgerEntry
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.commons.numbers import Amount, Quantity
from pypara.commons.zeitgeist import DateRange

# Helper to create a simple account
def make_account(name: str) -> Account:
    return Account(name=name)

# Helper to create a simple journal entry with one posting
def make_journal_entry(date: datetime.date, amount: Decimal, direction: int, account: Account) -> JournalEntry:
    posting = Posting(
        account=account,
        amount=Amount(amount),
        direction=direction,
        journal=None  # will be set after creation
    )
    journal = JournalEntry(
        description="Test",
        date=date,
        postings=[posting]
    )
    posting.journal = journal
    return journal

def test_ledger_initial_balance_and_add():
    """Ledger starts with the initial balance and updates correctly after adding a posting."""
    acc = make_account("Cash")
    ledger = Ledger(account=acc, initial=Quantity(Decimal("100.00")))
    # No entries yet, last balance should equal initial
    assert ledger._last_balance == Decimal("100.00")

    # Add a debit posting of 50
    journal = make_journal_entry(datetime.date(2023, 1, 1), Decimal("50.00"), direction=1, account=acc)
    entry = ledger.add(journal.postings[0])

    # After adding, balance should be 150
    assert entry.balance == Decimal("150.00")
    assert ledger._last_balance == Decimal("150.00")
    # Entry properties
    assert entry.date == datetime.date(2023, 1, 1)
    assert entry.description == "Test"
    assert entry.amount == Amount(Decimal("50.00"))
    assert entry.is_debit is True
    assert entry.is_credit is False
    assert entry.debit == Amount(Decimal("50.00"))
    assert entry.credit is None

def test_ledger_entry_counter_accounts_and_credit():
    """LedgerEntry correctly identifies counter accounts and credit amounts."""
    acc1 = make_account("Revenue")
    acc2 = make_account("Cash")
    # Credit posting to Revenue of 200
    journal = make_journal_entry(datetime.date(2023, 2, 1), Decimal("200.00"), direction=-1, account=acc1)
    # Add counter posting to Cash
    counter_posting = Posting(
        account=acc2,
        amount=Amount(Decimal("200.00")),
        direction=1,
        journal=journal
    )
    journal.postings.append(counter_posting)

    ledger = Ledger(account=acc1, initial=Quantity(Decimal("0.00")))
    entry = ledger.add(journal.postings[0])

    # Counter accounts should include Cash
    assert acc2 in entry.cntraccts
    # Credit amount should be present
    assert entry.is_credit is True
    assert entry.credit == Amount(Decimal("200.00"))
    assert entry.debit is None

def test_ledger_entry_multiple_postings_and_balance():
    """Adding multiple postings updates the ledger balance cumulatively."""
    acc = make_account("Inventory")
    ledger = Ledger(account=acc, initial=Quantity(Decimal("500.00")))

    # First debit of 100
    journal1 = make_journal_entry(datetime.date(2023, 3, 1), Decimal("100.00"), direction=1, account=acc)
    ledger.add(journal1.postings[0])

    # Second credit of 50
    journal2 = make_journal_entry(datetime.date(2023, 3, 2), Decimal("50.00"), direction=-1, account=acc)
    ledger.add(journal2.postings[0])

    # Final balance should be 550
    assert ledger._last_balance == Decimal("550.00")
