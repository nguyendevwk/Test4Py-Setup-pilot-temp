import datetime
from decimal import Decimal
import pytest
from pypara.accounting.ledger import (
    compile_general_ledger_program,
    build_general_ledger,
    GeneralLedger,
    Ledger,
    LedgerEntry,
)
from pypara.accounting.journaling import JournalEntry, Posting
from pypara.accounting.accounts import Account
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Quantity, Amount


# Helper to create a simple posting
def make_posting(account: Account, amount: Decimal, direction: int, date: datetime.date):
    return Posting(
        account=account,
        amount=Amount(amount),
        direction=direction,
        date=date,
    )


def make_journal_entry(date: datetime.date, postings):
    return JournalEntry(date=date, postings=postings)


def test_compile_program_normal_flow(tmp_path):
    """Verify that the compiled program builds a ledger with expected balances."""
    # Setup accounts
    acc_cash = Account("Cash")
    acc_sales = Account("Sales")

    # Initial balances
    initial_balances = {acc_cash: Ledger(acc_cash, Balance(datetime.date(2023, 12, 31), Quantity(Decimal("1000"))))}

    # Journal entries within period
    entries = [
        make_journal_entry(
            datetime.date(2024, 1, 15),
            [make_posting(acc_cash, Decimal("-200"), 1, datetime.date(2024, 1, 15)),
             make_posting(acc_sales, Decimal("200"), 1, datetime.date(2024, 1, 15))],
        )
    ]

    # Define read functions
    def read_initial_balances(period: DateRange):
        return initial_balances

    def read_journal_entries(period: DateRange):
        return entries

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)

    period = DateRange(datetime.date(2024, 1, 1), datetime.date(2024, 1, 31))
    ledger = program(period)

    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == period
    # Cash ledger should have initial 1000 and one posting -200
    cash_ledger = ledger.ledgers[acc_cash]
    assert len(cash_ledger.entries) == 1
    assert cash_ledger.entries[0].balance == Quantity(Decimal("800"))
    # Sales ledger should start at 0 and have +200
    sales_ledger = ledger.ledgers[acc_sales]
    assert len(sales_ledger.entries) == 1
    assert sales_ledger.entries[0].balance == Quantity(Decimal("200"))


def test_boundary_inclusion(tmp_path):
    """Entries exactly on the period boundaries should be included."""
    acc = Account("Revenue")
    initial_balances = {}
    entries = [
        make_journal_entry(
            datetime.date(2024, 1, 1),
            [make_posting(acc, Decimal("100"), 1, datetime.date(2024, 1, 1))],
        ),
        make_journal_entry(
            datetime.date(2024, 1, 31),
            [make_posting(acc, Decimal("-50"), 1, datetime.date(2024, 1, 31))],
        ),
    ]

    def read_initial_balances(period: DateRange):
        return initial_balances

    def read_journal_entries(period: DateRange):
        return entries

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)
    period = DateRange(datetime.date(2024, 1, 1), datetime.date(2024, 1, 31))
    ledger = program(period)

    revenue_ledger = ledger.ledgers[acc]
    assert len(revenue_ledger.entries) == 2
    assert revenue_ledger.entries[0].balance == Quantity(Decimal("100"))
    assert revenue_ledger.entries[1].balance == Quantity(Decimal("50"))


def test_no_entries_and_no_initial(tmp_path):
    """When there are no initial balances and no journal entries, the ledger should be empty."""
    def read_initial_balances(period: DateRange):
        return {}

    def read_journal_entries(period: DateRange):
        return []

    program = compile_general_ledger_program(read_initial_balances, read_journal_entries)
    period = DateRange(datetime.date(2024, 1, 1), datetime.date(2024, 1, 31))
    ledger = program(period)

    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == period
    assert ledger.ledgers == {}
