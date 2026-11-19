import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import build_general_ledger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance, Ledger, GeneralLedger
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Quantity


def test_build_general_ledger_with_initial_and_postings(tmp_path):
    """Ledger should start with initial balances and include all postings within the period."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc_cash = Account("Cash")
    acc_sales = Account("Sales")

    initial = {acc_cash: Balance(period.since, Quantity(Decimal("1000")))}
    postings = [
        JournalEntry(
            date=datetime.date(2023, 6, 15),
            postings=[
                Posting(acc_cash, Quantity(Decimal("-200"))),
                Posting(acc_sales, Quantity(Decimal("200"))),
            ],
        ),
        JournalEntry(
            date=datetime.date(2023, 12, 31),
            postings=[
                Posting(acc_cash, Quantity(Decimal("-100"))),
                Posting(acc_sales, Quantity(Decimal("100"))),
            ],
        ),
    ]

    ledger = build_general_ledger(period, postings, initial)

    # Check that initial balance is preserved
    assert ledger.ledgers[acc_cash].balance.amount == Decimal("1000")
    # Check that postings were applied
    assert ledger.ledgers[acc_cash].balance.amount == Decimal("700")
    assert ledger.ledgers[acc_sales].balance.amount == Decimal("300")
    # Ledger should contain both accounts
    assert set(ledger.ledgers.keys()) == {acc_cash, acc_sales}


def test_build_general_ledger_boundary_dates(tmp_path):
    """Postings on the boundary dates of the period should be included."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Revenue")
    initial = {}
    postings = [
        JournalEntry(
            date=period.since,
            postings=[Posting(acc, Quantity(Decimal("50")))],
        ),
        JournalEntry(
            date=period.until,
            postings=[Posting(acc, Quantity(Decimal("70")))],
        ),
    ]

    ledger = build_general_ledger(period, postings, initial)

    assert ledger.ledgers[acc].balance.amount == Decimal("120")
    assert len(ledger.ledgers[acc].postings) == 2


def test_build_general_ledger_excludes_out_of_range_postings(tmp_path):
    """Postings outside the period should not affect the ledger."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Expenses")
    initial = {acc: Balance(period.since, Quantity(Decimal("0")))}

    postings = [
        JournalEntry(
            date=datetime.date(2022, 12, 31),
            postings=[Posting(acc, Quantity(Decimal("-30")))],
        ),
        JournalEntry(
            date=datetime.date(2024, 1, 1),
            postings=[Posting(acc, Quantity(Decimal("-40")))],
        ),
    ]

    ledger = build_general_ledger(period, postings, initial)

    # No postings should have been applied
    assert ledger.ledgers[acc].balance.amount == Decimal("0")
    assert len(ledger.ledgers[acc].postings) == 0
