import datetime
from decimal import Decimal
import pytest

from pypara.accounting.ledger import build_general_ledger, GeneralLedger, Ledger, LedgerEntry
from pypara.accounting.accounts import Account
from pypara.accounting.journaling import JournalEntry, Posting, ReadJournalEntries
from pypara.commons.numbers import Amount, Quantity
from pypara.commons.zeitgeist import DateRange


def test_build_general_ledger_basic():
    # Setup period and accounts
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc_cash = Account("Cash")
    acc_sales = Account("Sales")

    # Initial balances
    initial = {acc_cash: Quantity(Decimal("1000.00"))}

    # Create journal entries
    je1 = JournalEntry(
        date=datetime.date(2023, 3, 15),
        description="Sale",
        postings=[
            Posting(account=acc_sales, amount=Amount(Decimal("200.00")), direction=Posting.DIRECTION.CREDIT),
            Posting(account=acc_cash, amount=Amount(Decimal("200.00")), direction=Posting.DIRECTION.DEBIT),
        ],
    )
    je2 = JournalEntry(
        date=datetime.date(2023, 6, 10),
        description="Purchase",
        postings=[
            Posting(account=acc_cash, amount=Amount(Decimal("50.00")), direction=Posting.DIRECTION.CREDIT),
            Posting(account=Account("Supplies"), amount=Amount(Decimal("50.00")), direction=Posting.DIRECTION.DEBIT),
        ],
    )

    # Build ledger
    gl = build_general_ledger(period, [je1, je2], initial)

    # Assertions
    assert isinstance(gl, GeneralLedger)
    assert gl.period == period
    # Cash ledger should have initial + two postings
    cash_ledger = gl.ledgers[acc_cash]
    assert isinstance(cash_ledger, Ledger)
    assert cash_ledger.account == acc_cash
    assert cash_ledger.initial.value == Decimal("1000.00")
    # Entries count
    assert len(cash_ledger.entries) == 2
    # Final balance calculation
    last_entry = cash_ledger.entries[-1]
    expected_balance = Decimal("1000.00") + Decimal("200.00") - Decimal("50.00")
    assert last_entry.balance.value == expected_balance

    # Sales ledger should have one entry
    sales_ledger = gl.ledgers[acc_sales]
    assert len(sales_ledger.entries) == 1
    sales_entry = sales_ledger.entries[0]
    assert sales_entry.is_credit
    assert sales_entry.credit == Amount(Decimal("200.00"))
    assert sales_entry.debit is None


def test_build_general_ledger_period_filtering():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 6, 30))
    acc = Account("Revenue")
    initial = {}

    je_in = JournalEntry(
        date=datetime.date(2023, 5, 20),
        description="In period",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("300.00")), direction=Posting.DIRECTION.CREDIT),
        ],
    )
    je_out = JournalEntry(
        date=datetime.date(2023, 7, 1),
        description="Out of period",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("400.00")), direction=Posting.DIRECTION.CREDIT),
        ],
    )

    gl = build_general_ledger(period, [je_in, je_out], initial)

    # Only the in-period entry should be present
    ledger = gl.ledgers[acc]
    assert len(ledger.entries) == 1
    entry = ledger.entries[0]
    assert entry.date == datetime.date(2023, 5, 20)
    assert entry.credit == Amount(Decimal("300.00"))
    assert entry.debit is None


def test_build_general_ledger_missing_initial_balance():
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    acc = Account("Expense")
    initial = {}

    je = JournalEntry(
        date=datetime.date(2023, 4, 5),
        description="Expense entry",
        postings=[
            Posting(account=acc, amount=Amount(Decimal("150.00")), direction=Posting.DIRECTION.DEBIT),
        ],
    )

    gl = build_general_ledger(period, [je], initial)

    ledger = gl.ledgers[acc]
    # Initial balance should default to zero
    assert ledger.initial.value == Decimal("0")
    # Entry should reflect debit
    entry = ledger.entries[0]
    assert entry.is_debit
    assert entry.debit == Amount(Decimal("150.00"))
    assert entry.credit is None
    # Balance after entry
    assert entry.balance.value == Decimal("150.00")
