import datetime
import pytest
from pypara.accounting.journaling import Posting, Direction
from pypara.accounting.accounts import Account, AccountType
from pypara.commons.numbers import Amount


def test_posting_debit_and_credit_logic():
    """Posting.is_debit correctly reflects account type and direction."""
    # Create a dummy journal placeholder
    class DummyJournal:
        pass

    journal = DummyJournal()

    # Asset account should be debit when direction is INC
    asset_account = Account(name="Cash", type=AccountType.ASSETS)
    posting_inc = Posting(
        journal=journal,
        date=datetime.date.today(),
        account=asset_account,
        direction=Direction.INC,
        amount=Amount(100),
    )
    assert posting_inc.is_debit is True
    assert posting_inc.is_credit is False

    # Revenue account should be credit when direction is INC
    revenue_account = Account(name="Sales", type=AccountType.REVENUES)
    posting_inc_rev = Posting(
        journal=journal,
        date=datetime.date.today(),
        account=revenue_account,
        direction=Direction.INC,
        amount=Amount(200),
    )
    assert posting_inc_rev.is_debit is False
    assert posting_inc_rev.is_credit is True

    # Expense account should be debit when direction is DEC
    expense_account = Account(name="Rent", type=AccountType.EXPENSES)
    posting_dec = Posting(
        journal=journal,
        date=datetime.date.today(),
        account=expense_account,
        direction=Direction.DEC,
        amount=Amount(50),
    )
    assert posting_dec.is_debit is True
    assert posting_dec.is_credit is False


def test_posting_amount_and_date_storage():
    """Posting stores the provided amount and date unchanged."""
    class DummyJournal:
        pass

    journal = DummyJournal()
    date = datetime.date(2023, 12, 31)
    account = Account(name="Inventory", type=AccountType.ASSETS)
    amount = Amount(1234.56)

    posting = Posting(
        journal=journal,
        date=date,
        account=account,
        direction=Direction.DEC,
        amount=amount,
    )

    assert posting.date == date
    assert posting.amount == amount
    assert posting.account is account
    assert posting.direction == Direction.DEC


def test_direction_of_quantity_zero_raises():
    """Direction.of raises AssertionError when quantity is zero."""
    from pypara.commons.numbers import Quantity

    zero_qty = Quantity(0)
    with pytest.raises(AssertionError, match="Encountered a `0` quantity"):
        Direction.of(zero_qty)
