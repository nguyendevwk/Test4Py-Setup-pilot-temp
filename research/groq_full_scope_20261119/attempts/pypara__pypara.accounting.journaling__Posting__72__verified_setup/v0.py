import datetime
import pytest
from pypara.accounting.journaling import Posting, Direction
from pypara.accounting.accounts import Account, AccountType
from pypara.commons.guid import makeguid
from pypara.commons.numbers import Amount


def test_posting_debit_and_credit_detection():
    """Posting.is_debit and is_credit correctly reflect account type and direction."""
    # Create a debit account and a credit account
    debit_account = Account(id=makeguid(), name="Cash", type=AccountType.ASSET)
    credit_account = Account(id=makeguid(), name="Revenue", type=AccountType.REVENUE)

    # Dummy journal placeholder (not used in the test)
    class DummyJournal:
        pass

    # Posting to debit account
    debit_posting = Posting(
        journal=DummyJournal(),
        date=datetime.date.today(),
        account=debit_account,
        direction=Direction.DEBIT,
        amount=Amount(100),
    )
    assert debit_posting.is_debit is True
    assert debit_posting.is_credit is False

    # Posting to credit account
    credit_posting = Posting(
        journal=DummyJournal(),
        date=datetime.date.today(),
        account=credit_account,
        direction=Direction.CREDIT,
        amount=Amount(200),
    )
    assert credit_posting.is_debit is False
    assert credit_posting.is_credit is True


def test_posting_zero_amount_handling():
    """Posting with zero amount still respects debit/credit logic."""
    zero_account = Account(id=makeguid(), name="Zero", type=AccountType.LIABILITY)
    dummy_journal = object()

    zero_posting = Posting(
        journal=dummy_journal,
        date=datetime.date.today(),
        account=zero_account,
        direction=Direction.CREDIT,
        amount=Amount(0),
    )
    # Even with zero amount, the direction and account type determine debit/credit
    assert zero_posting.is_debit is False
    assert zero_posting.is_credit is True


def test_posting_invalid_direction_raises_value_error():
    """Providing an invalid direction raises a ValueError during Posting initialization."""
    # Define a fake direction that is not part of the Direction enum
    class FakeDirection:
        pass

    account = Account(id=makeguid(), name="Test", type=AccountType.ASSET)
    dummy_journal = object()

    with pytest.raises(ValueError):
        Posting(
            journal=dummy_journal,
            date=datetime.date.today(),
            account=account,
            direction=FakeDirection(),  # type: ignore[arg-type]
            amount=Amount(50),
        )
