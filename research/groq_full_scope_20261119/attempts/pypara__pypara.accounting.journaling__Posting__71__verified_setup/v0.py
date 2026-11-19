import datetime
import pytest
from pypara.accounting.journaling import Posting, Direction, _debit_mapping
from pypara.accounting.accounts import Account, AccountType
from pypara.commons.numbers import Amount


def test_posting_debit_and_credit_flags():
    """Posting should correctly report debit/credit status based on account type and direction."""
    # Pick an account type that is known to be debit for a debit direction
    account = Account(name="Cash", type=AccountType.ASSET)
    # Create a dummy journal entry placeholder (any object works for the type hint)
    dummy_journal = object()
    posting = Posting(
        journal=dummy_journal,
        date=datetime.date.today(),
        account=account,
        direction=Direction.DEBIT,
        amount=Amount(100.0),
    )
    # The account type should be in the mapping for a debit direction
    assert posting.is_debit is True
    assert posting.is_credit is False

    # Now test the opposite direction
    posting_credit = Posting(
        journal=dummy_journal,
        date=datetime.date.today(),
        account=account,
        direction=Direction.CREDIT,
        amount=Amount(50.0),
    )
    # For a credit direction the same account type should not be considered debit
    assert posting_credit.is_debit is False
    assert posting_credit.is_credit is True


def test_posting_amount_and_date_storage():
    """Posting should store the provided amount and date unchanged."""
    account = Account(name="Revenue", type=AccountType.REVENUE)
    dummy_journal = object()
    test_date = datetime.date(2024, 1, 15)
    test_amount = Amount(1234.56)
    posting = Posting(
        journal=dummy_journal,
        date=test_date,
        account=account,
        direction=Direction.CREDIT,
        amount=test_amount,
    )
    assert posting.date == test_date
    assert posting.amount == test_amount
    # Ensure the amount is stored as an absolute value (non-negative)
    assert posting.amount >= 0


def test_posting_invalid_direction_raises():
    """Providing an invalid direction should raise a TypeError during initialization."""
    account = Account(name="Liability", type=AccountType.LIABILITY)
    dummy_journal = object()
    # Direction is expected to be an enum member; passing a string should fail
    with pytest.raises(TypeError):
        Posting(
            journal=dummy_journal,
            date=datetime.date.today(),
            account=account,
            direction="INVALID_DIRECTION",  # type: ignore[arg-type]
            amount=Amount(200.0),
        )
