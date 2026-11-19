import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import build_general_ledger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Quantity


def test_build_general_ledger_with_initial_and_entries():
    # Period
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))

    # Accounts
    cash = Account("Cash")
    revenue = Account("Revenue")

    # Initial balances
    initial = {cash: Balance(period.since, Quantity(Decimal("1000.00")))}

    # Journal entries
    entries = [
        JournalEntry(
            date=datetime.date(2023, 6, 15),
            postings=[
                Posting(account=cash, amount=Quantity(Decimal("200.00"))),
                Posting(account=revenue, amount=Quantity(Decimal("-200.00"))),
            ],
        ),
        JournalEntry(
            date=datetime.date(2023, 9, 10),
            postings=[
                Posting(account=cash, amount=Quantity(Decimal("-50.00"))),
                Posting(account=revenue, amount=Quantity(Decimal("50.00"))),
            ],
        ),
    ]

    ledger = build_general_ledger(period, entries, initial)

    # Check that both accounts exist in the ledger
    assert cash in ledger.ledgers
    assert revenue in ledger.ledgers

    # Verify balances
    cash_balance = ledger.ledgers[cash].balance
    revenue_balance = ledger.ledgers[revenue].balance

    assert cash_balance.amount == Decimal("1150.00")
    assert revenue_balance.amount == Decimal("-150.00")


def test_build_general_ledger_includes_boundary_dates():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acct = Account("Bank")
    initial = {acct: Balance(period.since, Quantity(Decimal("500.00")))}

    entries = [
        JournalEntry(
            date=period.since,
            postings=[Posting(account=acct, amount=Quantity(Decimal("100.00")))],
        ),
        JournalEntry(
            date=period.until,
            postings=[Posting(account=acct, amount=Quantity(Decimal("-50.00")))],
        ),
    ]

    ledger = build_general_ledger(period, entries, initial)

    final_balance = ledger.ledgers[acct].balance.amount
    assert final_balance == Decimal("550.00")  # 500 + 100 - 50


def test_build_general_ledger_no_initial_and_no_entries():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    initial = {}
    entries = []

    ledger = build_general_ledger(period, entries, initial)

    # Ledger should be empty
    assert len(ledger.ledgers) == 0
