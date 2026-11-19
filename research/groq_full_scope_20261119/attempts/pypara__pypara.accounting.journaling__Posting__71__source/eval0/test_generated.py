import datetime
import pytest
from pypara.accounting.journaling import Posting, Direction
from pypara.accounting.accounts import Account, AccountType

# Helper to create a minimal JournalEntry stub
class DummyJournal:
    pass

def test_posting_is_debit_and_credit_logic():
    """Verify that is_debit and is_credit properties reflect the account type and direction."""
    # Debit direction should be considered a debit for a normal account
    posting_debit = Posting(
        journal=DummyJournal(),
        date=datetime.date.today(),
        account=Account(name="Cash", type=AccountType.ASSET),
        direction=Direction.DEBIT,
        amount=100.0,
    )
    assert posting_debit.is_debit is True
    assert posting_debit.is_credit is False

    # Credit direction should be considered a credit for the same account
    posting_credit = Posting(
        journal=DummyJournal(),
        date=datetime.date.today(),
        account=Account(name="Cash", type=AccountType.ASSET),
        direction=Direction.CREDIT,
        amount=100.0,
    )
    assert posting_credit.is_debit is False
    assert posting_credit.is_credit is True

def test_posting_amount_boundary_zero():
    """Posting with zero amount should still correctly report debit/credit status."""
    posting_zero = Posting(
        journal=DummyJournal(),
        date=datetime.date.today(),
        account=Account(name="Revenue", type=AccountType.REVENUE),
        direction=Direction.CREDIT,
        amount=0.0,
    )
    # Zero amount does not change debit/credit logic
    assert posting_zero.is_debit is False
    assert posting_zero.is_credit is True

def test_posting_invalid_direction_raises():
    """Providing an invalid direction type should raise a TypeError."""
    with pytest.raises(TypeError):
        Posting(
            journal=DummyJournal(),
            date=datetime.date.today(),
            account=Account(name="Expense", type=AccountType.EXPENSE),
            direction="INVALID",  # not a Direction enum
            amount=50.0,
        )
