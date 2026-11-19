import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import build_general_ledger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.commons.zeitgeist import DateRange
from pypara.accounting.commons.numbers import Quantity


def test_build_general_ledger_normal():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Cash")
    posting = Posting(acc, Quantity(Decimal("100.00")))
    entry = JournalEntry(datetime.date(2023, 6, 15), [posting])
    initial = {}
    ledger = build_general_ledger(period, [entry], initial)

    # The ledger should contain one account with the correct balance
    assert acc in ledger.ledgers
    ledger_balance = ledger.ledgers[acc].balance
    assert ledger_balance.amount == Decimal("100.00")
    assert ledger_balance.date == datetime.date(2023, 1, 1)


def test_build_general_ledger_boundary_dates():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Revenue")
    # Posting exactly on the start date
    posting_start = Posting(acc, Quantity(Decimal("50.00")))
    entry_start = JournalEntry(datetime.date(2023, 1, 1), [posting_start])
    # Posting exactly on the end date
    posting_end = Posting(acc, Quantity(Decimal("75.00")))
    entry_end = JournalEntry(datetime.date(2023, 12, 31), [posting_end])

    initial = {}
    ledger = build_general_ledger(period, [entry_start, entry_end], initial)

    # Both postings should be included
    ledger_balance = ledger.ledgers[acc].balance
    assert ledger_balance.amount == Decimal("125.00")
    assert ledger_balance.date == datetime.date(2023, 1, 1)


def test_build_general_ledger_excludes_out_of_range():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Expense")
    # Posting outside the period
    posting = Posting(acc, Quantity(Decimal("200.00")))
    entry = JournalEntry(datetime.date(2024, 1, 1), [posting])

    initial = {}
    ledger = build_general_ledger(period, [entry], initial)

    # No ledger should be created for the account
    assert acc not in ledger.ledgers
