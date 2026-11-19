import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import build_general_ledger
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.generic import Balance
from pypara.accounting.generic import Ledger, GeneralLedger
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Quantity


def test_build_general_ledger_with_initial_and_postings(tmp_path):
    """Normal case: initial balances and postings within period are recorded."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc_cash = Account("Cash")
    acc_sales = Account("Sales")

    initial = {acc_cash: Balance(period.since, Quantity(Decimal("1000.00")))}

    entry = JournalEntry(
        date=datetime.date(2023, 6, 15),
        postings=[
            Posting(acc_cash, Quantity(Decimal("-200.00"))),
            Posting(acc_sales, Quantity(Decimal("200.00"))),
        ],
    )

    ledger = build_general_ledger(period, [entry], initial)

    # Verify that the ledger contains both accounts
    assert acc_cash in ledger.ledgers
    assert acc_sales in ledger.ledgers

    # Verify balances after posting
    cash_balance = ledger.ledgers[acc_cash].balance
    sales_balance = ledger.ledgers[acc_sales].balance
    assert cash_balance.amount == Decimal("800.00")
    assert sales_balance.amount == Decimal("200.00")


def test_build_general_ledger_boundary_dates(tmp_path):
    """Boundary case: postings exactly on the period boundaries are included."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Revenue")

    initial = {}

    entry_start = JournalEntry(
        date=period.since,
        postings=[Posting(acc, Quantity(Decimal("500.00")))],
    )
    entry_end = JournalEntry(
        date=period.until,
        postings=[Posting(acc, Quantity(Decimal("300.00")))],
    )

    ledger = build_general_ledger(period, [entry_start, entry_end], initial)

    # Verify that both postings are included
    balance = ledger.ledgers[acc].balance
    assert balance.amount == Decimal("800.00")


def test_build_general_ledger_excludes_out_of_range(tmp_path):
    """Error case: postings outside the period are ignored."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Expense")

    initial = {}

    entry_before = JournalEntry(
        date=datetime.date(2022, 12, 31),
        postings=[Posting(acc, Quantity(Decimal("100.00")))],
    )
    entry_after = JournalEntry(
        date=datetime.date(2024, 1, 1),
        postings=[Posting(acc, Quantity(Decimal("200.00")))],
    )
    entry_inside = JournalEntry(
        date=datetime.date(2023, 6, 1),
        postings=[Posting(acc, Quantity(Decimal("300.00")))],
    )

    ledger = build_general_ledger(period, [entry_before, entry_inside, entry_after], initial)

    # Only the inside entry should be present
    assert acc in ledger.ledgers
    assert ledger.ledgers[acc].balance.amount == Decimal("300.00")
    # No other accounts should exist
    assert len(ledger.ledgers) == 1
